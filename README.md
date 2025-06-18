# Video Semantic Search

A powerful semantic search application that enables you to search through video content using natural language queries. This tool processes video files, extracts meaningful information, and allows you to find specific moments or topics within your video library using AI-powered semantic understanding.

## 🎥 Demo

[View Demo Video](https://drive.google.com/file/d/1nm80d3X_grSBXQ9FEq0mtKeErT6is5L9/view?usp=sharing)

## ✨ Features

- **Semantic Video Search**: Search through video content using natural language queries
- **Vector Database Storage**: Efficient storage and retrieval using AstraDB
- **Interactive Web Interface**: User-friendly Streamlit-based UI
- **Multi-modal Processing**: Handles both video and audio content
- **Real-time Results**: Fast semantic search with relevance scoring

## 🛠️ Prerequisites

- Python 3.12.3+ (recommended)
- AstraDB account (DataStax)
- Internet connection for API calls

## 📋 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Scharlotten/videosemanticsearch.git
cd video-semantic-search
```

### 2. Set up AstraDB

#### Create an AstraDB Account
1. Visit [DataStax Astra](https://astra.datastax.com/)
2. Sign up for a free account
3. Create a new database:
   - Choose "Serverless (Non-Vector)" or "Vector Database" depending on your needs
   - Select your preferred cloud provider and region
   - Note down your database details

#### Generate API Credentials
1. In your AstraDB dashboard, navigate to "Settings" → "Application Tokens"
2. Generate a new token with the following roles:
   - Database Administrator (recommended for development)
3. Save the following credentials:
   - **Database ID**
   - **Application Token**
   - **API Endpoint**

#### Create Collections
Create the following collections in your AstraDB database:
1. **swimming** - For storing swimming-related video data
2. **audio** - For storing audio-extracted content

### 3. Environment Configuration

1. Copy the environment template:
```bash
cp .env_template .env
```

2. Edit the `.env` file and fill in your AstraDB credentials:
```env
ASTRA_DB_APPLICATION_TOKEN = 
ASTRA_DB_API_ENDPOINT = 
COLLECTION=
VIDEO=
OPENAI_API_KEY=
AUDIO_COLLECTION=
LANGFLOW_AUTHORIZATION=

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note**: Make sure you're using Python 3.12.3 or later for optimal compatibility.

### 5. Run the Application

Launch the Streamlit web interface:

```bash
streamlit run ui.py
```

The application will open in your default web browser, typically at `http://localhost:8501`.

## 🚀 Usage

1. **Upload Videos**: Use the web interface to upload your video files
2. **Processing**: The application will automatically extract and vectorize the content
3. **Search**: Enter natural language queries to find relevant video segments
4. **Results**: Browse through semantically matched results with relevance scores


## 🔧 Technologies Used

- **[Streamlit](https://streamlit.io/)** - Interactive web applications for machine learning and data science
- **[AstraDB](https://astra.datastax.com/)** - Cloud-native, multi-cloud database-as-a-service built on Apache Cassandra
- **Python 3.12.3** - Core programming language
- **Vector Embeddings** - For semantic search capabilities

## 📚 About the Technologies

### Streamlit
Streamlit is an open-source Python library that makes it easy to create beautiful, custom web applications for machine learning and data science projects. It allows you to turn data scripts into shareable web apps in minutes without requiring frontend development experience.

### AstraDB by DataStax
AstraDB is a cloud-native database built on Apache Cassandra, offering:
- Serverless, pay-per-request pricing
- Built-in vector search capabilities
- Multi-cloud availability
- Enterprise-grade security and compliance

## 🔍 Troubleshooting

### Common Issues

1. **Environment Variables Not Loaded**
   - Ensure your `.env` file is in the root directory
   - Check that all required variables are set
   - Restart the application after making changes


### Getting Help

- [Streamlit Documentation](https://docs.streamlit.io/)
- [AstraDB Documentation](https://docs.datastax.com/en/astra/docs/)
- [DataStax Community](https://community.datastax.com/)


## 🔗 Useful Links

- [Streamlit Gallery](https://streamlit.io/gallery) - Inspiration for Streamlit apps
- [AstraDB Free Tier](https://astra.datastax.com/register) - Get started with AstraDB
- [DataStax Academy](https://academy.datastax.com/) - Free courses on database technologies
- [Python Virtual Environments Guide](https://docs.python.org/3/tutorial/venv.html)

---

**Happy Searching!** 🎬✨