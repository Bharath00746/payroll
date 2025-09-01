import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from chatbot.models import Employees

class FAISSVectorDB:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.employee_ids = []
        self.create_index()

    def create_index(self):
        employees = Employees.objects.all()
        if not employees:
            return  # Prevent empty list crash

        texts = []
        self.employee_ids = []

        for emp in employees:
            texts.append(
                f"Name: {emp.name}, Age: {emp.age}, Mobile Number: {emp.mobile_number}, "
                f"Date of Birth: {emp.date_of_birth}, "
                f"Date of Joining: {emp.date_of_joining}, "
                f"Taken Leave: {emp.taken_leave}, "
                f"Available Leave: {emp.available_leave}, "
                f"Sick Leave: {emp.sick_leave}, "
                f"Casual Leave: {emp.casual_leave}, "
                f"Aadhar Number: {emp.aadhar_number}, "
                f"PAN Card Number: {emp.pan_card_number}"
            )
            self.employee_ids.append(emp.employee_id)

        embeddings = self.model.encode(texts, convert_to_tensor=False)
        embeddings = np.array(embeddings).astype('float32')

        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)

    def search(self, query, k=1):
        if self.index is None or not self.employee_ids:
            return []

        query_embedding = self.model.encode([query], convert_to_tensor=False)
        query_embedding = np.array(query_embedding).astype('float32')

        distances, indices = self.index.search(query_embedding, k)

        results = []
        for i, idx in enumerate(indices[0]):
            if 0 <= idx < len(self.employee_ids):
                emp_id = self.employee_ids[idx]
                dist = distances[0][i]
                results.append((emp_id, dist))

        return results
