from transformers import pipeline, set_seed
import torch
import tensorflow as tf
from sklearn.model_selection import train_test_split
import re
from transformers import GPT2Tokenizer, GPT2Model
from transformers import TextDataset,DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments,AutoModelWithLMHead

# input_data = list of string utterances

def build_model(input_data, output_dir):
    print("Building model...")
    
    train, test = train_test_split(input_data,test_size=0.15) 
    build_text_files(train,'train_dataset.txt')
    build_text_files(test,'test_dataset.txt')
    
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

    train_path = 'train_dataset.txt'
    test_path = 'test_dataset.txt'

    train_dataset,test_dataset,data_collator = load_dataset(train_path,test_path,tokenizer)

    model = AutoModelWithLMHead.from_pretrained('gpt2')


    training_args = TrainingArguments(
        output_dir=output_dir, #The output directory
        overwrite_output_dir=True, #overwrite the content of the output directory
        num_train_epochs=3, # number of training epochs
        per_device_train_batch_size=32, # batch size for training
        per_device_eval_batch_size=64,  # batch size for evaluation
        eval_steps = 400, # Number of update steps between two evaluations.
        save_steps=800, # after # steps model is saved 
        warmup_steps=500,# number of warmup steps for learning rate scheduler
        prediction_loss_only=True,
        )


    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
    )
    
    trainer.train()
    trainer.save_model(output_dir)
    print("Model built!")



def build_text_files(the_data, dest_path):
    print("building text file...")
    f = open(dest_path, 'w')
    data = ''
    for texts in the_data:
            summary = re.sub(r"\s", " ", texts)
            data += summary + "  "
    f.write(data)

def load_dataset(train_path,test_path,tokenizer):
    print("loading dataset...")
    train_dataset = TextDataset(
          tokenizer=tokenizer,
          file_path=train_path,
          block_size=128)
     
    test_dataset = TextDataset(
          tokenizer=tokenizer,
          file_path=test_path,
          block_size=128)   
    
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, mlm=False,
    )
    return train_dataset,test_dataset,data_collator

# build_model(all_data)
# gen = pipeline('text-generation',model='./gpt2-sandbox', tokenizer='gpt2',config={'max_length':800})
# gen("I think")
