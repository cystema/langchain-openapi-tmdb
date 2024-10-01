import os
import yaml
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_community.agent_toolkits.openapi.spec import reduce_openapi_spec
from langchain_community.utilities.requests import RequestsWrapper
from langchain_community.agent_toolkits.openapi import planner
from langchain_openai import ChatOpenAI
from fastapi.responses import StreamingResponse
import tiktoken
from dotenv import load_dotenv
import uvicorn

app = FastAPI()

ALLOW_DANGEROUS_REQUEST = True

load_dotenv()

# Load API keys and other environment variables
def construct_tmdb_auth_headers():
    tmdb_api_key = os.getenv("TMDB_API_KEY")
    if not tmdb_api_key:
        raise ValueError("TMDB API key not found in environment variables.")
    return {"Authorization": f"Bearer {tmdb_api_key}", "accept": "application/json"}


# Headers for TMDB API
headers = construct_tmdb_auth_headers()
requests_wrapper = RequestsWrapper(headers=headers)

# Load the TMDB OpenAPI spec
with open("api_spec/tmdb_openapi.yaml") as f:
    raw_tmdb_api_spec = yaml.load(f, Loader=yaml.Loader)
tmdb_api_spec = reduce_openapi_spec(raw_tmdb_api_spec)

# Set up the OpenAI LLM for LangChain
llm = ChatOpenAI(
    model_name="gpt-4", 
    temperature=0.0, 
    api_key=os.getenv('OPENAI_API_KEY')
)

# Create the TMDB agent using LangChain planner
tmdb_agent = planner.create_openapi_agent(
    tmdb_api_spec,
    requests_wrapper,
    llm,
    allow_dangerous_requests=ALLOW_DANGEROUS_REQUEST,
    verbose=True,
    return_intermediate_steps=True,
)

# Define input structure for user query using Pydantic
class UserQuery(BaseModel):
    query: str

# API endpoint for movie recommendations
@app.post("/movie/")
async def get_movie_recommendations(user_query: UserQuery):
    async def generate():
        try:
            # Stream events from the agent
            async for event in tmdb_agent.astream_events(
                {"input": user_query.query}, version="v1"
            ):
                kind = event["event"]
                
                # # Handle start of chain execution
                if kind == "on_chain_start":
                    # yield f"Starting agent: {event['name']} with input: {event['data']['input']}\n"
                    yield f"Starting agent: {event['name']}.\n"
                
                # Handle end of chain execution
                elif kind == "on_chain_end":
                    # yield f"{event['name']} agent done.  with output: {event['data']['output']}\n"
                    yield f"{event['name']} agent done.\n"
                
                # Handle intermediate steps streamed from the model
                if kind == "on_chat_model_stream":
                    content = event["data"]["chunk"].content
                    if content:
                        yield content
        
        except Exception as e:
            yield f"Error: {str(e)}\n"
            raise HTTPException(status_code=500, detail=str(e))

    # Return a streaming response to the client
    return StreamingResponse(generate(), media_type="text/plain")

# Adds routes to the app for using the chain under:
# /invoke
# /batch
# /stream
# /stream_events
# add_routes(
#     app,
#     RunnableLambda(get_movie_recommendations),
# )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)



