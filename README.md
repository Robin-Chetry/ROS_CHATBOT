# ROS Chatbot

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-Framework-green)](https://www.langchain.com/)
[![Pinecone](https://img.shields.io/badge/Pinecone-VectorDB-orange)](https://www.pinecone.io/)
[![Flask](https://img.shields.io/badge/Flask-Backend-black)](https://flask.palletsprojects.com/)

A complete **ROS-integrated AI chatbot** powered by **Large Language Models (LLMs)**, **LangChain**, **Pinecone**, **Flask**, and **AWS**.
This chatbot is designed as a **ROS Assistant**, enabling intelligent, context-aware conversations.

---

## Features

* Conversational Memory – remembers past interactions
* LangChain-powered LLM integration
* Pinecone Vector Database for knowledge retrieval
* Flask backend for serving API endpoints
* Embeddings storage & retrieval for persistent context
* AWS deployment-ready

---

## Tech Stack

* Python
* LangChain
* Flask
* Gemini API
* Pinecone
* AWS (for deployment)

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Robin-Chetry/ROS_CHATBOT.git
cd ROS_CHATBOT
```

### 2. Activate virtual environment

```bash
projenv/Scripts/activate   # For Windows
# OR
source projenv/bin/activate  # For Linux/Mac
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add environment variables

Create a `.env` file in the **root directory** and add your credentials:

```env
PINECONE_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
GEMINI_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### 5. Store embeddings in Pinecone

```bash
python store_index.py
```

### 6. Run the Flask server

```bash
python app.py
```

---

## Access the Chatbot

Once the server is running, open:

```
http://localhost:5000
```

---

## Project Structure

```
ROS_CHATBOT/
│── app.py                # Flask backend API
│── store_index.py         # Script to store embeddings in Pinecone
│── requirements.txt       # Python dependencies
│── .env                   # API keys (not committed)
│── templates/             # HTML frontend
│── static/                # CSS & JS files
└── projenv/               # Virtual environment
```

---

## License

This project is licensed under the MIT License.

---

## Contributing

Pull requests are welcome! If you want to improve the chatbot or add more integrations, fork the repo and submit a PR.

---

## Screenshot

![Chatbot UI Preview](https://via.placeholder.com/1000x500.png?text=ROS+Chatbot+UI)

---

## Author

Developed by **Robin Rawat**
Contact: [robin.rawat@example.com](mailto:robin.rawat@example.com)
GitHub: [Robin-Chetry](https://github.com/Robin-Chetry)
