import pandas as pd
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, Trainer, TrainingArguments
from sklearn.preprocessing import LabelEncoder
import torch
import joblib

class SerenityModel:
    def __init__(self):
        self.tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
        self.model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=6)  # Adjust num_labels based on your labels
        self.encoder = LabelEncoder()
        self.train_model()

    def train_model(self):
        train = pd.read_csv("train.csv", delimiter=';')
        test = pd.read_csv("test.csv", delimiter=';')
        
        # Encode labels
        labels = self.encoder.fit_transform(train['label'])
        train_texts = train['message'].tolist()
        test_texts = test['message'].tolist()
        
        # Tokenize data
        train_encodings = self.tokenizer(train_texts, truncation=True, padding=True, max_length=128)
        test_encodings = self.tokenizer(test_texts, truncation=True, padding=True, max_length=128)
        
        # Create dataset
        class EmotionDataset(torch.utils.data.Dataset):
            def __init__(self, encodings, labels):
                self.encodings = encodings
                self.labels = labels
            def __getitem__(self, idx):
                item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
                item['labels'] = torch.tensor(self.labels[idx])
                return item
            def __len__(self):
                return len(self.labels)
        
        train_dataset = EmotionDataset(train_encodings, labels)
        test_dataset = EmotionDataset(test_encodings, self.encoder.transform(test['label']))
        
        # Training arguments
        training_args = TrainingArguments(
            output_dir='./results',
            num_train_epochs=3,
            per_device_train_batch_size=8,
            per_device_eval_batch_size=8,
            warmup_steps=500,
            weight_decay=0.01,
            logging_dir='./logs',
            evaluation_strategy="epoch"
        )
        
        # Trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=test_dataset
        )
        trainer.train()
        
        # Save model
        self.model.save_pretrained("serenity_model")
        self.tokenizer.save_pretrained("serenity_model")
        joblib.dump(self.encoder, "encoder.pkl")

    def predict(self, message):
        inputs = self.tokenizer(message, return_tensors="pt", truncation=True, padding=True, max_length=128)
        outputs = self.model(**inputs)
        probs = outputs.logits.softmax(dim=1)
        pred_idx = probs.argmax().item()
        prob = probs[0][pred_idx].item()
        label = self.encoder.inverse_transform([pred_idx])[0]
        return label, prob

if __name__ == "__main__":
    model = SerenityModel()
    label, prob = model.predict("I feel really sad today")
    print(f"Predicted: {label}, Probability: {prob:.2f}")