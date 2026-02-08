# Langflow Nodes Organization

## FAISS
- **FAISS**: FAISS Vector Store with search capabilities (Icon: FAISS)

## Notion
- **Add Content to Page **: Convert markdown text to Notion blocks and append them to a Notion page. (Icon: NotionDirectoryLoader)
- **Create Page **: A component for creating Notion pages. (Icon: NotionDirectoryLoader)
- **List Database Properties **: Retrieve properties of a Notion database. (Icon: NotionDirectoryLoader)
- **List Pages **: Query a Notion database with filtering and sorting. The input should be a JSON string containing the 'filter' and 'sorts' objects. Example input:
{"filter": {"property": "Status", "select": {"equals": "Done"}}, "sorts": [{"timestamp": "created_time", "direction": "descending"}]} (Icon: NotionDirectoryLoader)
- **List Users **: Retrieve users from Notion. (Icon: NotionDirectoryLoader)
- **Page Content Viewer **: Retrieve the content of a Notion page as plain text. (Icon: NotionDirectoryLoader)
- **Search **: Searches all pages and databases that have been shared with an integration. (Icon: NotionDirectoryLoader)
- **Update Page Property **: Update the properties of a Notion page. (Icon: NotionDirectoryLoader)

## agentql
- **Extract Web Data**: Extracts structured data from a web page using an AgentQL query or a Natural Language description. (Icon: AgentQL)

## aiml
- **AI/ML API**: Generates text using AI/ML API LLMs. (Icon: AIML)
- **AI/ML API Embeddings**: Generate embeddings using the AI/ML API. (Icon: AIML)

## altk
- **ALTK Agent** (Beta): Advanced agent with both pre-tool validation and post-tool processing capabilities. (Icon: zap)

## amazon
- **Amazon Bedrock** (Legacy): Generate text using Amazon Bedrock LLMs with the legacy ChatBedrock API. This component is deprecated. Please use Amazon Bedrock Converse instead for better compatibility, newer features, and improved conversation handling. (Icon: Amazon)
- **Amazon Bedrock Converse** (Beta): Generate text using Amazon Bedrock LLMs with the modern Converse API for improved conversation handling. (Icon: Amazon)
- **Amazon Bedrock Embeddings**: Generate embeddings using Amazon Bedrock models. (Icon: Amazon)
- **S3 Bucket Uploader**: Uploads files to S3 bucket. (Icon: Amazon)

## anthropic
- **Anthropic**: Generate text using Anthropic's Messages API and models. (Icon: Anthropic)

## apify
- **Apify Actors**: Use Apify Actors to extract data from hundreds of places fast. This component can be used in a flow to retrieve data or as a tool with an agent. (Icon: Apify)

## arxiv
- **arXiv**: Search and retrieve papers from arXiv.org (Icon: arXiv)

## assemblyai
- **AssemblyAI Get Subtitles**: Export your transcript in SRT or VTT format for subtitles and closed captions (Icon: AssemblyAI)
- **AssemblyAI LeMUR**: Apply Large Language Models to spoken data using the AssemblyAI LeMUR framework (Icon: AssemblyAI)
- **AssemblyAI List Transcripts**: Retrieve a list of transcripts from AssemblyAI with filtering options (Icon: AssemblyAI)
- **AssemblyAI Poll Transcript**: Poll for the status of a transcription job using AssemblyAI (Icon: AssemblyAI)
- **AssemblyAI Start Transcript**: Create a transcription job for an audio file using AssemblyAI with advanced options (Icon: AssemblyAI)

## azure
- **Azure OpenAI**: Generate text using Azure OpenAI LLMs. (Icon: Azure)
- **Azure OpenAI Embeddings**: Generate embeddings using Azure OpenAI models. (Icon: Azure)

## baidu
- **Qianfan**: Generate text using Baidu Qianfan LLMs. (Icon: BaiduQianfan)

## bing
- **Bing Search API**: Call the Bing Search API. (Icon: Bing)

## cassandra
- **Cassandra**: Cassandra Vector Store with search capabilities (Icon: Cassandra)
- **Cassandra Chat Memory**: Retrieves and store chat messages from Apache Cassandra. (Icon: Cassandra)
- **Cassandra Graph**: Cassandra Graph Vector Store (Icon: Cassandra)

## chroma
- **Chroma DB**: Chroma Vector Store with search capabilities (Icon: Chroma)

## cleanlab
- **Cleanlab Evaluator**: Evaluates any LLM response using Cleanlab and outputs trust score and explanation. (Icon: Cleanlab)
- **Cleanlab RAG Evaluator**: Evaluates context, query, and response from a RAG pipeline using Cleanlab and outputs trust metrics. (Icon: Cleanlab)
- **Cleanlab Remediator**: Remediates an untrustworthy response based on trust score from the Cleanlab Evaluator, score threshold, and message handling settings. (Icon: Cleanlab)

## clickhouse
- **ClickHouse**: ClickHouse Vector Store with search capabilities (Icon: Clickhouse)

## cloudflare
- **Cloudflare Workers AI Embeddings**: Generate embeddings using Cloudflare Workers AI models. (Icon: Cloudflare)

## cohere
- **Cohere Embeddings**: Generate embeddings using Cohere models. (Icon: Cohere)
- **Cohere Language Models**: Generate text using Cohere LLMs. (Icon: Cohere)
- **Cohere Rerank**: Rerank documents using the Cohere API. (Icon: Cohere)

## cometapi
- **CometAPI**: All AI Models in One API 500+ AI Models (Icon: CometAPI)

## composio
- **AgentQL**:  (Icon: AgentQL)
- **Agiled**:  (Icon: Agiled)
- **Airtable**:  (Icon: Airtable)
- **Apollo**:  (Icon: Apollo)
- **Asana**:  (Icon: Asana)
- **Attio**:  (Icon: Attio)
- **Bitbucket**:  (Icon: Bitbucket)
- **Bolna**:  (Icon: Bolna)
- **Brightdata**:  (Icon: Brightdata)
- **Calendly**:  (Icon: Calendly)
- **Canva**:  (Icon: Canva)
- **Canvas**:  (Icon: Canvas)
- **Coda**:  (Icon: Coda)
- **Composio Tools**: Use Composio toolset to run actions with your agent (Icon: Composio)
- **Contentful**:  (Icon: Contentful)
- **Digicert**:  (Icon: Digicert)
- **Discord**:  (Icon: discord)
- **Dropbox**:  (Icon: Dropbox)
- **ElevenLabs**:  (Icon: Elevenlabs)
- **Exa**:  (Icon: ExaComposio)
- **Figma**:  (Icon: Figma)
- **Finage**:  (Icon: Finage)
- **Firecrawl**:  (Icon: Firecrawl)
- **Fireflies**:  (Icon: Fireflies)
- **Fixer**:  (Icon: Fixer)
- **Flexisign**:  (Icon: Flexisign)
- **Freshdesk**:  (Icon: Freshdesk)
- **GitHub**:  (Icon: Github)
- **Gmail**:  (Icon: Gmail)
- **Google Classroom**:  (Icon: Classroom)
- **GoogleBigQuery**:  (Icon: Googlebigquery)
- **GoogleCalendar**:  (Icon: Googlecalendar)
- **GoogleDocs**:  (Icon: Googledocs)
- **GoogleMeet**:  (Icon: Googlemeet)
- **GoogleSheets**:  (Icon: Googlesheets)
- **GoogleTasks**:  (Icon: GoogleTasks)
- **Heygen**:  (Icon: Heygen)
- **Instagram**:  (Icon: Instagram)
- **Jira**:  (Icon: Jira)
- **Jotform**:  (Icon: Jotform)
- **Klaviyo**:  (Icon: Klaviyo)
- **Linear**:  (Icon: Linear)
- **Listennotes**:  (Icon: Listennotes)
- **Mem0**:  (Icon: Mem0Composio)
- **Miro**:  (Icon: Miro)
- **Missive**:  (Icon: Missive)
- **Notion**:  (Icon: Notion)
- **OneDrive**:  (Icon: One_Drive)
- **Outlook**:  (Icon: Outlook)
- **Pandadoc**:  (Icon: Pandadoc)
- **PeopleDataLabs**:  (Icon: Peopledatalabs)
- **PerplexityAI**:  (Icon: PerplexityComposio)
- **Reddit**:  (Icon: Reddit)
- **SerpAPI**:  (Icon: SerpSearchComposio)
- **Slack**:  (Icon: SlackComposio)
- **Slackbot**:  (Icon: SlackComposio)
- **Snowflake**:  (Icon: Snowflake)
- **Supabase**:  (Icon: Supabase)
- **Tavily**:  (Icon: Tavily)
- **TimelinesAI**:  (Icon: Timelinesai)
- **Todoist**:  (Icon: Todoist)
- **Wrike**:  (Icon: Wrike)
- **YouTube**:  (Icon: YouTube)

## confluence
- **Confluence**: Confluence wiki collaboration platform (Icon: Confluence)

## couchbase
- **Couchbase**: Couchbase Vector Store with search capabilities (Icon: Couchbase)

## crewai
- **CrewAI Agent** (Legacy): Represents an agent of CrewAI. (Icon: CrewAI)
- **Hierarchical Crew** (Legacy): Represents a group of agents, defining how they should collaborate and the tasks they should perform. (Icon: CrewAI)
- **Hierarchical Task** (Legacy): Each task must have a description, an expected output and an agent responsible for execution. (Icon: CrewAI)
- **Sequential Crew** (Legacy): Represents a group of agents with tasks that are executed sequentially. (Icon: CrewAI)
- **Sequential Task** (Legacy): Each task must have a description, an expected output and an agent responsible for execution. (Icon: CrewAI)
- **Sequential Task Agent** (Legacy): Creates a CrewAI Task and its associated Agent. (Icon: CrewAI)

## cuga
- **Cuga**: Define the Cuga agent's instructions, then assign it a task. (Icon: bot)

## custom_component
- **Custom Component**: Use as a template to create your own component. (Icon: code)

## data_source
- **API Request**: Make HTTP requests using URL or cURL commands. (Icon: Globe)
- **Load CSV** (Legacy): Load a CSV file, CSV from a file path, or a valid CSV string and convert it to a list of Data (Icon: file-spreadsheet)
- **Load JSON** (Legacy): Convert a JSON file, JSON from a file path, or a JSON string to a Data object or a list of Data objects (Icon: braces)
- **Mock Data**: Generate mock data for testing and development. (Icon: database)
- **News Search** (Legacy): Searches Google News via RSS. Returns clean article data. (Icon: newspaper)
- **RSS Reader** (Legacy): Fetches and parses an RSS feed. (Icon: rss)
- **SQL Database**: Executes SQL queries on SQLAlchemy-compatible databases. (Icon: database)
- **URL**: Fetch content from one or more web pages, following links recursively. (Icon: layout-template)
- **Web Search**: Search the web, news, or RSS feeds. (Icon: search)

## datastax
- **Astra Assistant Agent** (Legacy): Manages Assistant Interactions (Icon: AstraDB)
- **Astra DB**: Ingest and search documents in Astra DB (Icon: AstraDB)
- **Astra DB CQL**: Create a tool to get transactional data from DataStax Astra DB CQL Table (Icon: AstraDB)
- **Astra DB Chat Memory**: Retrieves and stores chat messages from Astra DB. (Icon: AstraDB)
- **Astra DB Graph** (Legacy): Implementation of Graph Vector Store using Astra DB (Icon: AstraDB)
- **Astra DB Tool** (Legacy): Tool to run hybrid vector and metadata search on DataStax Astra DB Collection (Icon: AstraDB)
- **Astra Vectorize** (Legacy): Configuration options for Astra Vectorize server-side embeddings.  (Icon: AstraDB)
- **Create Assistant** (Legacy): Creates an Assistant and returns it's id (Icon: AstraDB)
- **Create Assistant Thread** (Legacy): Creates a thread and returns the thread id (Icon: AstraDB)
- **Dotenv** (Legacy): Load .env file into env vars (Icon: AstraDB)
- **Get Assistant name** (Legacy): Assistant by id (Icon: AstraDB)
- **Get Environment Variable** (Legacy): Gets the value of an environment variable from the system. (Icon: AstraDB)
- **Graph RAG**: Graph RAG traversal for vector store. (Icon: AstraDB)
- **Hyper-Converged Database**: Implementation of Vector Store using Hyper-Converged Database (HCD) with search capabilities (Icon: HCD)
- **List Assistants** (Legacy): Returns a list of assistant id's (Icon: AstraDB)
- **Run Assistant** (Legacy): Executes an Assistant Run against a thread (Icon: AstraDB)

## deepseek
- **DeepSeek**: Generate text using DeepSeek LLMs. (Icon: DeepSeek)

## docling
- **Chunk DoclingDocument**: Use the DocumentDocument chunkers to split the document into chunks. (Icon: Docling)
- **Docling**: Uses Docling to process input documents running the Docling models locally. (Icon: Docling)
- **Docling Serve**: Uses Docling to process input documents connecting to your instance of Docling Serve. (Icon: Docling)
- **Export DoclingDocument**: Export DoclingDocument to markdown, html or other formats. (Icon: Docling)

## duckduckgo
- **DuckDuckGo Search**: Search the web using DuckDuckGo with customizable result limits (Icon: DuckDuckGo)

## elastic
- **Elasticsearch**: Elasticsearch Vector Store with with advanced, customizable search capabilities. (Icon: ElasticsearchStore)
- **OpenSearch**: Store and search documents using OpenSearch with hybrid semantic and keyword search capabilities. (Icon: OpenSearch)

## embeddings
- **Embedding Similarity** (Legacy): Compute selected form of similarity between two embedding vectors. (Icon: equal)
- **Text Embedder** (Legacy): Generate embeddings for a given message using the specified embedding model. (Icon: binary)

## exa
- **Exa Search** (Beta): Exa Search toolkit for search and content retrieval (Icon: ExaSearch)

## files_and_knowledge
- **Directory**: Recursively load files from a directory. (Icon: folder)
- **Knowledge Ingestion**: Create or update knowledge in Langflow. (Icon: upload)
- **Knowledge Retrieval**: Search and retrieve data from knowledge. (Icon: download)
- **Read File**: Loads and returns the content from uploaded files. (Icon: file-text)
- **Write File**: Save data to local file, AWS S3, or Google Drive in the selected format. (Icon: file-text)

## firecrawl
- **Firecrawl Crawl API**: Crawls a URL and returns the results. (Icon: )
- **Firecrawl Extract API**: Extracts data from a URL. (Icon: )
- **Firecrawl Map API**: Maps a URL and returns the results. (Icon: )
- **Firecrawl Scrape API**: Scrapes a URL and returns the results. (Icon: )

## flow_controls
- **Condition** (Legacy): Route Data object(s) based on a condition applied to a specified key, including boolean validation. (Icon: split)
- **Flow as Tool** (Legacy): Construct a Tool from a function that runs the loaded Flow. (Icon: hammer)
- **If-Else**: Routes an input message to a corresponding output based on text comparison. (Icon: split)
- **Listen** (Beta): A component to listen for a notification. (Icon: Radio)
- **Loop**: Iterates over a list of Data or Message objects, outputting one item at a time and aggregating results from loop inputs. Message objects are automatically converted to Data objects for consistent processing. (Icon: infinity)
- **Notify** (Beta): A component to generate a notification to Get Notified component. (Icon: Notify)
- **Pass** (Legacy): Forwards the input message, unchanged. (Icon: arrow-right)
- **Run Flow** (Beta): Executes another flow from within the same project. Can also be used as a tool for agents. 
 **Select a Flow to use the tool mode** (Icon: Workflow)
- **Sub Flow** (Legacy): Generates a Component from a Flow, with all of its inputs, and  (Icon: Workflow)

## git
- **Git**: Load and filter documents from a local or remote Git repository. Use a local repo path or clone from a remote URL. (Icon: GitLoader)
- **GitExtractor**: Analyzes a Git repository and returns file contents and complete repository information (Icon: GitLoader)

## glean
- **Glean Search API**: Search using Glean's API. (Icon: Glean)

## google
- **BigQuery** (Beta): Execute SQL queries on Google BigQuery. (Icon: Google)
- **Gmail Loader** (Legacy): Loads emails from Gmail using provided credentials. (Icon: Google)
- **Google Drive Loader** (Legacy): Loads documents from Google Drive using provided credentials. (Icon: Google)
- **Google Drive Search** (Legacy): Searches Google Drive files using provided credentials and query parameters. (Icon: Google)
- **Google Generative AI**: Generate text using Google Generative AI. (Icon: GoogleGenerativeAI)
- **Google Generative AI Embeddings**: Connect to Google's generative AI embeddings service using the GoogleGenerativeAIEmbeddings class, found in the langchain-google-genai package. (Icon: GoogleGenerativeAI)
- **Google OAuth Token** (Legacy): Generates a JSON string with your Google OAuth token. (Icon: Google)
- **Google Search API**: Call Google Search API and return results as a DataFrame. (Icon: Google)
- **Google Serper API**: Call the Serper.dev Google Search API. (Icon: Serper)

## groq
- **Groq**: Generate text using Groq. (Icon: Groq)

## homeassistant
- **Home Assistant Control**: A very simple tool to control Home Assistant devices. Only action (turn_on, turn_off, toggle) and entity_id need to be provided. (Icon: HomeAssistant)
- **List Home Assistant States**: Retrieve states from Home Assistant. The agent only needs to specify 'filter_domain' (optional). Token and base_url are not exposed to the agent. (Icon: HomeAssistant)

## huggingface
- **Hugging Face**: Generate text using Hugging Face Inference APIs. (Icon: HuggingFace)
- **Hugging Face Embeddings Inference**: Generate embeddings using Hugging Face Text Embeddings Inference (TEI) (Icon: HuggingFace)

## ibm
- **IBM watsonx.ai**: Generate text using IBM watsonx.ai foundation models. (Icon: WatsonxAI)
- **IBM watsonx.ai Embeddings**: Generate embeddings using IBM watsonx.ai models. (Icon: WatsonxAI)

## icosacomputing
- **Combinatorial Reasoner**: Uses Combinatorial Optimization to construct an optimal prompt with embedded reasons. Sign up here:
https://forms.gle/oWNv2NKjBNaqqvCx6 (Icon: Icosa)

## input_output
- **Chat Input**: Get chat inputs from the Playground. (Icon: MessagesSquare)
- **Chat Output**: Display a chat message in the Playground. (Icon: MessagesSquare)
- **Text Input**: Get user text inputs. (Icon: type)
- **Text Output**: Sends text output via API. (Icon: type)
- **Webhook**:  (Icon: webhook)

## jigsawstack
- **AI Scraper**: Scrape any website instantly and get consistent structured data         in seconds without writing any css selector code (Icon: JigsawStack)
- **AI Web Search**: Effortlessly search the Web and get access to high-quality results powered with AI. (Icon: JigsawStack)
- **File Read**: Read any previously uploaded file seamlessly from         JigsawStack File Storage and use it in your AI applications. (Icon: JigsawStack)
- **File Upload**: Store any file seamlessly on JigsawStack File Storage and use it in your AI applications.         Supports various file types including images, documents, and more. (Icon: JigsawStack)
- **Image Generation**: Generate an image based on the given text by employing AI models like Flux,         Stable Diffusion, and other top models. (Icon: JigsawStack)
- **NSFW Detection**: Detect if image/video contains NSFW content (Icon: JigsawStack)
- **Object Detection**: Perform object detection on images using JigsawStack's Object Detection Model,         capable of image grounding, segmentation and computer use. (Icon: JigsawStack)
- **Sentiment Analysis**: Analyze sentiment of text using JigsawStack AI (Icon: JigsawStack)
- **Text Translate**: Translate text from one language to another with support for multiple text formats. (Icon: JigsawStack)
- **Text to SQL**: Convert natural language to SQL queries using JigsawStack AI (Icon: JigsawStack)
- **VOCR**: Extract data from any document type in a consistent structure with fine-tuned         vLLMs for the highest accuracy (Icon: JigsawStack)

## langchain_utilities
- **CSV Agent**: Construct a CSV agent from a CSV and tools. (Icon: LangChain)
- **Character Text Splitter**: Split text by number of characters. (Icon: LangChain)
- **ConversationChain** (Legacy): Chain to have a conversation and load context from memory. (Icon: LangChain)
- **Fake Embeddings**: Generate fake embeddings, useful for initial testing and connecting components. (Icon: LangChain)
- **HTML Link Extractor**: Extract hyperlinks from HTML content. (Icon: LangChain)
- **JsonAgent** (Legacy): Construct a json agent from an LLM and tools. (Icon: )
- **LLMCheckerChain** (Legacy): Chain for question-answering with self-verification. (Icon: LangChain)
- **LLMMathChain** (Legacy): Chain that interprets a prompt and executes python code to do math. (Icon: LangChain)
- **Language Recursive Text Splitter**: Split text into chunks of a specified length based on language. (Icon: LangChain)
- **Natural Language Text Splitter**: Split text based on natural language boundaries, optimized for a specified language. (Icon: LangChain)
- **Natural Language to SQL** (Legacy): Generate SQL from natural language. (Icon: LangChain)
- **OpenAI Tools Agent**: Agent that uses tools via openai-tools. (Icon: LangChain)
- **OpenAPI Agent**: Agent to interact with OpenAPI API. (Icon: LangChain)
- **Prompt Hub** (Beta): Prompt Component that uses LangChain Hub prompts (Icon: LangChain)
- **Recursive Character Text Splitter**: Split text trying to keep all related text together. (Icon: LangChain)
- **Retrieval QA** (Legacy): Chain for question-answering querying sources from a retriever. (Icon: LangChain)
- **Runnable Executor** (Beta): Execute a runnable. It will try to guess the input and output keys. (Icon: LangChain)
- **SQLAgent**: Construct an SQL agent from an LLM and tools. (Icon: LangChain)
- **SQLDatabase**: SQL Database (Icon: LangChain)
- **Self Query Retriever** (Legacy): Retriever that uses a vector store and an LLM to generate the vector store queries. (Icon: LangChain)
- **Semantic Text Splitter** (Beta): Split text into semantically meaningful chunks using semantic similarity. (Icon: LangChain)
- **Spider Web Crawler & Scraper**: Spider API for web crawling and scraping. (Icon: )
- **Tool Calling Agent**: An agent designed to utilize various tools seamlessly within workflows. (Icon: LangChain)
- **VectorStoreInfo** (Legacy): Information about a VectorStore (Icon: LangChain)
- **VectorStoreRouterAgent** (Legacy): Construct an agent from a Vector Store Router. (Icon: )
- **XML Agent** (Beta): Agent that uses tools formatting instructions as xml to the Language Model. (Icon: LangChain)

## langwatch
- **LangWatch Evaluator**: Evaluates various aspects of language models using LangWatch's evaluation endpoints. (Icon: Langwatch)

## llm_operations
- **Batch Run**: Runs an LLM on each row of a DataFrame column. If no column is specified, all columns are used. (Icon: List)
- **LLM Selector**: Routes the input to the most appropriate LLM based on OpenRouter model specifications (Icon: git-branch)
- **Smart Router**: Routes an input message using LLM-based categorization. (Icon: route)
- **Smart Transform**: Uses an LLM to generate a function for filtering or transforming structured data. (Icon: square-function)
- **Structured Output**: Uses an LLM to generate structured data. Ideal for extraction and consistency. (Icon: braces)

## lmstudio
- **LM Studio**: Generate text using LM Studio Local LLMs. (Icon: LMStudio)
- **LM Studio Embeddings**: Generate embeddings using LM Studio. (Icon: LMStudio)

## maritalk
- **MariTalk**: Generates text using MariTalk LLMs. (Icon: Maritalk)

## mem0
- **Mem0 Chat Memory**: Retrieves and stores chat messages using Mem0 memory storage. (Icon: Mem0)

## milvus
- **Milvus**: Milvus vector store with search capabilities (Icon: Milvus)

## mistral
- **MistralAI**: Generates text using MistralAI LLMs. (Icon: MistralAI)
- **MistralAI Embeddings**: Generate embeddings using MistralAI models. (Icon: MistralAI)

## models_and_agents
- **Agent**: Define the agent's instructions, then enter a task to complete using tools. (Icon: bot)
- **Embedding Model**: Generate embeddings using a specified provider. (Icon: binary)
- **Language Model**: Runs a language model given a specified provider. (Icon: brain-circuit)
- **MCP Tools**: Connect to an MCP server to use its tools. (Icon: Mcp)
- **Message History**: Stores or retrieves stored chat messages from Langflow tables or an external memory. (Icon: message-square-more)
- **Prompt Template**: Create a prompt template with dynamic variables. (Icon: braces)

## mongodb
- **MongoDB Atlas**: MongoDB Atlas Vector Store with search capabilities (Icon: MongoDB)

## needle
- **Needle Retriever**: A retriever that uses the Needle API to search collections. (Icon: Needle)

## notdiamond
- **Not Diamond Router**: Call the right model at the right time with the world's most powerful AI model router. (Icon: NotDiamond)

## novita
- **Novita AI**: Generates text using Novita AI LLMs (OpenAI compatible). (Icon: Novita)

## nvidia
- **NVIDIA**: Generates text using NVIDIA LLMs. (Icon: NVIDIA)
- **NVIDIA Embeddings**: Generate embeddings using NVIDIA models. (Icon: NVIDIA)
- **NVIDIA Rerank**: Rerank documents using the NVIDIA API. (Icon: NVIDIA)
- **NVIDIA Retriever Extraction** (Beta): Multi-modal data extraction from documents using NVIDIA's NeMo API. (Icon: NVIDIA)
- **NVIDIA System-Assist**: (Windows only) Prompts NVIDIA System-Assist to interact with the NVIDIA GPU Driver. The user may query GPU specifications, state, and ask the NV-API to perform several GPU-editing acations. The prompt must be human-readable language. (Icon: NVIDIA)

## olivya
- **Place Call**: A component to create an outbound call request from Olivya's platform. (Icon: Olivya)

## ollama
- **Ollama**: Generate text using Ollama Local LLMs. (Icon: Ollama)
- **Ollama Embeddings**: Generate embeddings using Ollama models. (Icon: Ollama)

## openai
- **OpenAI**: Generates text using OpenAI LLMs. (Icon: OpenAI)
- **OpenAI Embeddings**: Generate embeddings using OpenAI models. (Icon: OpenAI)

## openrouter
- **OpenRouter**: OpenRouter provides unified access to multiple AI models from different providers through a single API. (Icon: OpenRouter)

## perplexity
- **Perplexity**: Generate text using Perplexity LLMs. (Icon: Perplexity)

## pgvector
- **PGVector**: PGVector Vector Store with search capabilities (Icon: cpu)

## pinecone
- **Pinecone**: Pinecone Vector Store with search capabilities (Icon: Pinecone)

## processing
- **Alter Metadata** (Legacy): Adds/Removes Metadata Dictionary on inputs (Icon: merge)
- **Combine Data** (Legacy): Combines data using different operations (Icon: merge)
- **Combine Text** (Legacy): Concatenate two text sources into a single text chunk using a specified delimiter. (Icon: merge)
- **Create Data** (Legacy): Dynamically create a Data with a specified number of fields. (Icon: ListFilter)
- **Create List** (Legacy): Creates a list of texts. (Icon: list)
- **Data Operations**: Perform various operations on a Data object. (Icon: file-json)
- **Data to Message** (Legacy): Convert Data objects into Messages using any {field_name} from input data. (Icon: message-square)
- **Data → DataFrame** (Legacy): Converts one or multiple Data objects into a DataFrame. Each Data object corresponds to one row. Fields from `.data` become columns, and the `.text` (if present) is placed in a 'text' column. (Icon: table)
- **DataFrame Operations**: Perform various operations on a DataFrame. (Icon: table)
- **Dynamic Create Data**: Dynamically create a Data with a specified number of fields. (Icon: ListFilter)
- **Extract Key** (Legacy): Extract a specific key from a Data object or a list of Data objects and return the extracted value(s) as Data object(s). (Icon: key)
- **Filter Data** (Beta) (Legacy): Filters a Data object based on a list of keys. (Icon: filter)
- **Filter Values** (Beta) (Legacy): Filter a list of data items based on a specified key, filter value, and comparison operator. Check advanced options to select match comparision. (Icon: filter)
- **JSON Cleaner** (Legacy): Cleans the messy and sometimes incorrect JSON strings produced by LLMs so that they are fully compliant with the JSON spec. (Icon: braces)
- **Message Store** (Legacy): Stores a chat message or text into Langflow tables or an external memory. (Icon: message-square-text)
- **Message to Data** (Beta) (Legacy): Convert a Message object to a Data object (Icon: message-square-share)
- **Output Parser** (Legacy): Transforms the output of an LLM into a specified format. (Icon: type)
- **Parse DataFrame** (Legacy): Convert a DataFrame into plain text following a specified template. Each column in the DataFrame is treated as a possible template key, e.g. {col_name}. (Icon: braces)
- **Parse JSON** (Legacy): Convert and extract JSON fields. (Icon: braces)
- **Parser**: Extracts text using a template. (Icon: braces)
- **Regex Extractor** (Legacy): Extract patterns from text using regular expressions. (Icon: regex)
- **Select Data** (Legacy): Select a single data from a list of data. (Icon: prototypes)
- **Split Text**: Split text into chunks based on specified criteria. (Icon: scissors-line-dashed)
- **Type Convert**: Convert between different types (Message, Data, DataFrame) (Icon: repeat)
- **Update Data** (Legacy): Dynamically update or append data with the specified fields. (Icon: FolderSync)

## prototypes
- **Python Function** (Legacy): Define and execute a Python function that returns a Data object or a Message. (Icon: Python)

## qdrant
- **Qdrant**: Qdrant Vector Store with search capabilities (Icon: Qdrant)

## redis
- **Redis**: Implementation of Vector Store using Redis (Icon: Redis)
- **Redis Chat Memory**: Retrieves and store chat messages from Redis. (Icon: Redis)

## sambanova
- **SambaNova**: Generate text using Sambanova LLMs. (Icon: SambaNova)

## scrapegraph
- **ScrapeGraph Markdownify API**: Given a URL, it will return the markdownified content of the website. (Icon: )
- **ScrapeGraph Search API**: Given a search prompt, it will return search results using ScrapeGraph's search functionality. (Icon: ScrapeGraph)
- **ScrapeGraph Smart Scraper API**: Given a URL, it will return the structured data of the website. (Icon: )

## searchapi
- **SearchApi**: Calls the SearchApi API with result limiting. Supports Google, Bing and DuckDuckGo. (Icon: SearchAPI)

## serpapi
- **Serp Search API**: Call Serp Search API with result limiting (Icon: SerpSearch)

## supabase
- **Supabase**: Supabase Vector Store with search capabilities (Icon: Supabase)

## tavily
- **Tavily Extract API**: **Tavily Extract** extract raw content from URLs. (Icon: TavilyIcon)
- **Tavily Search API**: **Tavily Search** is a search engine optimized for LLMs and RAG,         aimed at efficient, quick, and persistent search results. (Icon: TavilyIcon)

## tools
- **Calculator** (Legacy): Perform basic arithmetic operations on a given expression. (Icon: calculator)
- **Google Search API [DEPRECATED]** (Legacy): Call Google Search API. (Icon: Google)
- **Google Serper API [DEPRECATED]** (Legacy): Call the Serper.dev Google Search API. (Icon: Google)
- **Python Code Structured** (Legacy): structuredtool dataclass code to tool (Icon: Python)
- **Python REPL** (Legacy): A tool for running Python code in a REPL environment. (Icon: Python)
- **SearXNG Search** (Legacy): A component that searches for tools using SearXNG. (Icon: )
- **Search API** (Legacy): Call the searchapi.io API with result limiting (Icon: SearchAPI)
- **Serp Search API** (Legacy): Call Serp Search API with result limiting (Icon: SerpSearch)
- **Tavily Search API** (Legacy): **Tavily Search API** is a search engine optimized for LLMs and RAG,         aimed at efficient, quick, and persistent search results. It can be used independently or as an agent tool.

Note: Check 'Advanced' for all options.
 (Icon: TavilyIcon)
- **Wikidata API** (Legacy): Performs a search using the Wikidata API. (Icon: Wikipedia)
- **Wikipedia API** (Legacy): Call Wikipedia API. (Icon: Wikipedia)
- **Yahoo! Finance** (Legacy): Uses [yfinance](https://pypi.org/project/yfinance/) (unofficial package) to access financial data and market information from Yahoo! Finance. (Icon: trending-up)

## twelvelabs
- **Convert Astra DB to Pegasus Input**: Converts Astra DB search results to inputs compatible with TwelveLabs Pegasus. (Icon: TwelveLabs)
- **Split Video**: Split a video into multiple clips of specified duration. (Icon: TwelveLabs)
- **TwelveLabs Pegasus**: Chat with videos using TwelveLabs Pegasus API. (Icon: TwelveLabs)
- **TwelveLabs Pegasus Index Video**: Index videos using TwelveLabs and add the video_id to metadata. (Icon: TwelveLabs)
- **TwelveLabs Text Embeddings**: Generate embeddings using TwelveLabs text embedding models. (Icon: TwelveLabs)
- **TwelveLabs Video Embeddings**: Generate embeddings from videos using TwelveLabs video embedding models. (Icon: TwelveLabs)
- **Video File**: Load a video file in common video formats. (Icon: TwelveLabs)

## unstructured
- **Unstructured API**: Uses Unstructured.io API to extract clean text from raw source documents. Supports a wide range of file types. (Icon: Unstructured)

## upstash
- **Upstash**: Upstash Vector Store with search capabilities (Icon: Upstash)

## utilities
- **Calculator**: Perform basic arithmetic operations on a given expression. (Icon: calculator)
- **Current Date**: Returns the current date and time in the selected timezone. (Icon: clock)
- **ID Generator** (Legacy): Generates a unique ID. (Icon: fingerprint)
- **Python Interpreter**: Run Python code with optional imports. Use print() to see the output. (Icon: square-terminal)

## vectara
- **Vectara**: Vectara Vector Store with search capabilities (Icon: Vectara)
- **Vectara RAG**: Vectara's full end to end RAG (Icon: Vectara)

## vectorstores
- **Local DB** (Legacy): Local Vector Store with search capabilities (Icon: database)

## vertexai
- **Vertex AI**: Generate text using Vertex AI LLMs. (Icon: VertexAI)
- **Vertex AI Embeddings**: Generate embeddings using Google Cloud Vertex AI models. (Icon: VertexAI)

## vlmrun
- **VLM Run Transcription** (Beta): Extract structured data from audio and video using [VLM Run AI](https://app.vlm.run) (Icon: VLMRun)

## weaviate
- **Weaviate**: Weaviate Vector Store with search capabilities (Icon: Weaviate)

## wikipedia
- **Wikidata**: Performs a search using the Wikidata API. (Icon: Wikipedia)
- **Wikipedia**: Call Wikipedia API. (Icon: Wikipedia)

## wolframalpha
- **WolframAlpha API**: Enables queries to WolframAlpha for computational data, facts, and calculations across various topics, delivering structured responses. (Icon: WolframAlphaAPI)

## xai
- **xAI**: Generates text using xAI models like Grok. (Icon: xAI)

## yahoosearch
- **Yahoo! Finance**: Uses [yfinance](https://pypi.org/project/yfinance/) (unofficial package) to access financial data and market information from Yahoo! Finance. (Icon: trending-up)

## youtube
- **YouTube Channel**: Retrieves detailed information and statistics about YouTube channels as a DataFrame. (Icon: YouTube)
- **YouTube Comments**: Retrieves and analyzes comments from YouTube videos. (Icon: YouTube)
- **YouTube Playlist**: Extracts all video URLs from a YouTube playlist. (Icon: YouTube)
- **YouTube Search**: Searches YouTube videos based on query. (Icon: YouTube)
- **YouTube Transcripts**: Extracts spoken content from YouTube videos with multiple output options. (Icon: YouTube)
- **YouTube Trending**: Retrieves trending videos from YouTube with filtering options. (Icon: YouTube)
- **YouTube Video Details**: Retrieves detailed information and statistics about YouTube videos. (Icon: YouTube)

## zep
- **Zep Chat Memory** (Legacy): Retrieves and store chat messages from Zep. (Icon: ZepMemory)

