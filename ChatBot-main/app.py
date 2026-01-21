from flask import Flask, render_template, request, jsonify
from brain import predict_class, get_response, intents  # Import from brain.py

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    
    # First, use the brain functions to classify the intent and get a response
    intent = predict_class(msg)  # Predict the intent based on the user's message
    response = get_response(intent)  # Get the response based on the intent

    # If the intent is one that should use the DialoGPT model for a more open-ended conversation
    if intent == 'open_chat':  # Assuming 'open_chat' is an intent handled by the DialoGPT model
        response = get_Chat_response(msg)
    
    return jsonify({'response': response})


def get_Chat_response(text):
    # Let's chat for 5 lines
    chat_history_ids = torch.tensor([])  # Initialize chat history tensor
    for step in range(5):
        # encode the new user input, add the eos_token and return a tensor in Pytorch
        new_user_input_ids = tokenizer.encode(str(text) + tokenizer.eos_token, return_tensors='pt')

        # append the new user input tokens to the chat history
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids

        # generate a response while limiting the total chat history to 1000 tokens
        chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

        # pretty print last output tokens from bot
        return tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)


if __name__ == '__main__':
    app.run()
