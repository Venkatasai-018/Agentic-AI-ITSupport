"""
RAG (Retrieval Augmented Generation) System
Uses sentence transformers and ChromaDB for semantic search
"""
import json
import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class RAGSystem:
    """RAG system for IT support knowledge retrieval"""
    
    def __init__(self, knowledge_base_path: str = "knowledge_base.json"):
        """Initialize RAG system with embeddings and vector database"""
        logger.info("Initializing RAG system...")
        
        # Load sentence transformer model for embeddings
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize ChromaDB
        self.client = chromadb.Client()
        
        # Create or get collection
        try:
            self.collection = self.client.get_collection(name="it_support_kb")
            logger.info("Loaded existing ChromaDB collection")
        except:
            self.collection = self.client.create_collection(name="it_support_kb")
            logger.info("Created new ChromaDB collection")
        
        self.knowledge_base_path = knowledge_base_path
        self.kb_data = []
        
        # Load knowledge base
        self.load_knowledge_base()
    
    def load_knowledge_base(self):
        """Load knowledge base and create embeddings"""
        try:
            with open(self.knowledge_base_path, 'r') as f:
                self.kb_data = json.load(f)
            
            # Check if collection is empty
            if self.collection.count() == 0:
                self._index_knowledge_base()
            else:
                logger.info(f"Using existing index with {self.collection.count()} documents")
                
        except FileNotFoundError:
            logger.warning(f"Knowledge base file not found: {self.knowledge_base_path}")
            self.kb_data = []
    
    def _index_knowledge_base(self):
        """Index knowledge base into vector database"""
        if not self.kb_data:
            logger.warning("No knowledge base data to index")
            return
        
        documents = []
        metadatas = []
        ids = []
        
        for idx, item in enumerate(self.kb_data):
            # Create rich document text for better semantic matching
            doc_text = f"""
            Category: {item['category']}
            Title: {item.get('title', item['category'])}
            Keywords: {', '.join(item['keywords'])}
            Description: {item.get('description', '')}
            Solution: {item['solution']}
            """.strip()
            
            documents.append(doc_text)
            metadatas.append({
                'category': item['category'],
                'auto_resolvable': str(item['auto_resolvable']),
                'priority': item['priority_level'],
                'title': item.get('title', item['category'])
            })
            ids.append(f"kb_doc_{idx}")
        
        # Add to ChromaDB
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        logger.info(f"✓ Indexed {len(documents)} documents into RAG system")
    
    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Semantic search for relevant knowledge base entries
        
        Args:
            query: User's IT support request
            top_k: Number of top results to return
            
        Returns:
            List of relevant knowledge base entries with similarity scores
        """
        if self.collection.count() == 0:
            logger.warning("ChromaDB collection is empty")
            return []
        
        # Query the vector database
        results = self.collection.query(
            query_texts=[query],
            n_results=min(top_k, self.collection.count())
        )
        
        # Format results
        relevant_items = []
        if results['ids'] and len(results['ids'][0]) > 0:
            for i in range(len(results['ids'][0])):
                doc_id = results['ids'][0][i]
                idx = int(doc_id.split('_')[-1])
                
                if idx < len(self.kb_data):
                    kb_entry = self.kb_data[idx]
                    relevant_items.append({
                        'category': kb_entry['category'],
                        'title': kb_entry.get('title', kb_entry['category']),
                        'description': kb_entry.get('description', ''),
                        'solution': kb_entry['solution'],
                        'auto_resolvable': kb_entry['auto_resolvable'],
                        'priority': kb_entry['priority_level'],
                        'keywords': kb_entry['keywords'],
                        'distance': results['distances'][0][i] if results['distances'] else None,
                        'relevance_score': 1 - results['distances'][0][i] if results['distances'] else 0.0
                    })
        
        return relevant_items
    
    def get_best_match(self, query: str) -> Optional[Dict[str, Any]]:
        """Get the single best matching solution"""
        results = self.search(query, top_k=1)
        return results[0] if results else None
    
    def add_knowledge_entry(self, entry: Dict[str, Any]) -> bool:
        """Add a new entry to the knowledge base"""
        try:
            # Add to in-memory data
            self.kb_data.append(entry)
            
            # Index in vector database
            idx = len(self.kb_data) - 1
            doc_text = f"""
            Category: {entry['category']}
            Title: {entry.get('title', entry['category'])}
            Keywords: {', '.join(entry['keywords'])}
            Description: {entry.get('description', '')}
            Solution: {entry['solution']}
            """.strip()
            
            self.collection.add(
                documents=[doc_text],
                metadatas=[{
                    'category': entry['category'],
                    'auto_resolvable': str(entry['auto_resolvable']),
                    'priority': entry['priority_level'],
                    'title': entry.get('title', entry['category'])
                }],
                ids=[f"kb_doc_{idx}"]
            )
            
            # Save to file
            with open(self.knowledge_base_path, 'w') as f:
                json.dump(self.kb_data, f, indent=2)
            
            logger.info(f"Added new knowledge entry: {entry['category']}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding knowledge entry: {e}")
            return False


# Global RAG instance
_rag_instance: Optional[RAGSystem] = None


def get_rag_system() -> RAGSystem:
    """Get or create global RAG system instance"""
    global _rag_instance
    if _rag_instance is None:
        _rag_instance = RAGSystem()
    return _rag_instance


# Test the RAG system
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    rag = RAGSystem()
    
    test_queries = [
        "I forgot my password and can't login",
        "My wifi is not working",
        "I need to install new software",
        "Printer is not responding"
    ]
    
    print("\n" + "="*60)
    print("Testing RAG System")
    print("="*60)
    
    for query in test_queries:
        print(f"\n Query: {query}")
        result = rag.get_best_match(query)
        if result:
            print(f"Category: {result['category']}")
            print(f"Relevance Score: {result['relevance_score']:.3f}")
            print(f"Auto-resolvable: {result['auto_resolvable']}")
