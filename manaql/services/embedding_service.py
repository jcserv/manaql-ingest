import os
import time
from typing import List

import voyageai

from common.color import Color
from database.models.card import Card


class EmbeddingService:
    """Service for generating and managing card embeddings using Voyage AI's voyage-3.5 model."""

    def __init__(self):
        self.client = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))
        self.model = "voyage-3.5"

    def generate_card_text(self, card: Card) -> str:
        """
        Generate a text representation of a card for embedding.
        This text should capture the card's characteristics for similarity search.
        """
        text_parts = []

        # Basic card info
        text_parts.append(f"Name: {card.name}")
        text_parts.append(f"Type: {card.type_line or card.main_type}")

        # Mana cost and CMC
        if card.mana_cost:
            text_parts.append(f"Mana Cost: {card.mana_cost}")
        if card.cmc is not None:
            text_parts.append(f"Converted Mana Cost: {card.cmc}")

        # Colors
        if card.colors:
            color_names = [Color(c).name for c in card.colors]
            text_parts.append(f"Colors: {', '.join(color_names)}")

        # Oracle text (rules text)
        if card.oracle_text:
            text_parts.append(f"Rules Text: {card.oracle_text}")

        # Keywords
        if card.keywords:
            text_parts.append(f"Keywords: {', '.join(card.keywords)}")

        # Power/Toughness for creatures
        if card.power and card.toughness:
            text_parts.append(f"Power/Toughness: {card.power}/{card.toughness}")

        # Game formats
        if card.games:
            text_parts.append(f"Available in: {', '.join(card.games)}")

        return " | ".join(text_parts)

    def generate_embedding(self, text: str) -> List[float]:
        """Generate an embedding for the given text using Voyage AI's API."""
        try:
            response = self.client.embed(
                [text], model=self.model, input_type="document"
            )
            return response.embeddings[0]
        except Exception as e:
            raise Exception(f"Failed to generate embedding: {str(e)}")

    def generate_card_embedding(self, card: Card) -> List[float]:
        """Generate an embedding for a card."""
        card_text = self.generate_card_text(card)
        return self.generate_embedding(card_text)

    def update_card_embedding(self, card: Card) -> None:
        """Update a card's embedding in the database."""
        embedding = self.generate_card_embedding(card)
        card.embedding = embedding
        card.save(update_fields=["embedding"])

    def batch_update_embeddings(self, cards: List[Card], batch_size: int = 128) -> None:
        """Update embeddings for multiple cards using Voyage's batch embedding API."""
        for i in range(0, len(cards), batch_size):
            batch = cards[i : i + batch_size]
            try:
                texts = [self.generate_card_text(card) for card in batch]
                response = self.client.embed(
                    texts, model=self.model, input_type="document"
                )
                for card, embedding in zip(batch, response.embeddings):
                    card.embedding = embedding
                    card.save(update_fields=["embedding"])
            except Exception as e:
                print(
                    f"Failed to update embeddings for batch starting at {i}: {str(e)}"
                )
                # Fall back to per-card to isolate failures
                for card in batch:
                    try:
                        self.update_card_embedding(card)
                    except Exception as inner:
                        print(
                            f"Failed to update embedding for card {card.name}: {str(inner)}"
                        )
            time.sleep(0.1)
