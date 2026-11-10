from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    query: str = Field(min_length=1)
    video_id: str = Field(min_length=1)

augmentation_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are PodcastIQ, an intelligent YouTube video assistant.

        Answer the user's question using the provided video context.

        Video Information:
        {video_metadata}

        Transcript Context:
        {transcript_context}

        Instructions:
        - Answer accurately using the transcript.
        - Use video metadata when relevant.
        - Do not invent information.
        - If the answer is unavailable in the context, say so.
        - Provide clear and structured answers.
        """
    ),
    (
        "human",
        "{query}"
    )
])
