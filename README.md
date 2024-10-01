### API Agent with LangChain OpenAPI Toolkit

This project demonstrates how to use the **LangChain OpenAPI Toolkit** to automatically interact with The Movie Database (TMDB) API (or any other API spec) based on user input. 

Using the LangChain OpenAPI Toolkit, this project takes in the TMDB OpenAPI specification, allowing an AI agent to understand and decide which TMDB API endpoints to call based on natural language queries from the user.

### Key Features:
- **Automated API Decision-Making**: Based on the user’s query, the LangChain agent determines which TMDB API endpoint to call by referencing the OpenAPI spec. This allows the agent to intelligently interact with the TMDB API and provide appropriate results (like movie search results, movie details, and more).
- **Natural Language Understanding**: Users can interact with the agent using natural language. The agent parses user input, determines intent, and decides the correct TMDB API endpoint to call (e.g., a user asking for a movie by name would trigger the search API).
- **Streaming Intermediate Steps**: The system provides real-time feedback to the user, streaming intermediate results as the agent processes and executes tasks.
    
### How It Works:
1. **TMDB OpenAPI Specification**: The TMDB API specification is loaded using the LangChain OpenAPI Toolkit. The spec provides the details of all available API endpoints, parameters, and responses.
2. **LangChain Planner**: The LangChain `planner` module uses the OpenAPI spec to dynamically generate agent actions. When a user provides input (e.g., "Show me details of the movie 'Inception'"), the agent consults the spec to determine which API endpoint to call (in this case, `GET /movie/{movie_id}`) and fetches the movie details.
3. **Automated API Calls**: The agent uses the OpenAPI spec to validate user requests, select the appropriate TMDB API endpoint, construct the correct API call, and fetch the results. The API responses are then streamed back to the user.
4. **Flexible Responses**: The agent dynamically builds responses based on the results of the TMDB API calls, such as providing movie details, actor information, or related recommendations.
    
### Example Interaction:

- **User**: "What is the plot of the movie 'The Dark Knight'?"
- **Agent**: Automatically recognizes that this query needs to call the `/movie/{movie_id}` endpoint from the TMDB API to fetch movie details, then returns the movie’s plot information.

### Setup Instructions:
1. Clone the repository.
2. Note: important files are in `api/tmdb-openapi-server`.
3. Install dependencies using `pip install -r requirements.txt` (in a venv, hopefully).
4. Set up your environment variables by creating a `.env` file with your `TMDB_API_KEY` and `OPENAI_API_KEY`.
5. Start the FastAPI server by running:
```bash
python3 server.py
```
6. Use the provided `curl` command to test the endpoint.

### Testing the API:
To test the API with `curl`, you can use the following command to post a movie-related query to the FastAPI server:

```bash
curl -X POST "http://0.0.0.0:8000/movie/" \
		-H "Content-Type: application/json" \
		-d '{"query": "What are some movies like The Matrix?"}'
```