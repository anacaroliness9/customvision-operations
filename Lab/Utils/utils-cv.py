from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import os 
import time

class CustomVisionProject:

    trainer = None
    predictor= None
    project = None

    def get_trainer(self,training_key, train_endpoint):
        credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
        self.trainer = CustomVisionTrainingClient(train_endpoint, credentials)
        return self.trainer

    def get_predictor(self,prediction_key, prediction_endpoint):
        prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
        self.predictor = CustomVisionPredictionClient(prediction_endpoint, prediction_credentials)
        return self.predictor

    def create_project(self,project_name):
        # Create a new project
        print ("Creating project...")
        self.project =  self.trainer.create_project(project_name)

    def get_project (self, project_id):
        self.project = self.trainer.get_project(project_id)

    def delete_project(self):
        print ("Deleting project...") 
        self.trainer.delete_project(self.project.id)
        
    def get_projects(self):
        return self.trainer.get_projects(raw=True).response.json()

    def get_tags(self):
        tags = list()
        for i in self.trainer.get_tags(self.project.id):
            tags.append( i.name)
        return tags

    def create_tags (self, tags):
        for i in tags:
            if i not in self.get_tags():
                self.trainer.create_tag(self.project.id, i)

    def upload_local_images(self,folder,tags_in=None):
        tags = self.trainer.get_tags(self.project.id)
        if tags_in is not None:
            tags = [i  for i in self.trainer.get_tags(self.project.id) if i.name in tags_in ]

        for tag in tags:
            print("Uploading images...")
            print("Uploading '{}' images:".format(tag.name))
            for image in os.listdir(os.path.join(folder,tag.name)):
                try:
                    image_data = open(os.path.join(folder,tag.name,image), "rb").read()
                    self.trainer.create_images_from_data(self.project.id, image_data, [tag.id])
                except:
                    print ("Error uploading {} image.".format(image))
                else:
                    print("Image {} sucessfully uploaded!".format(image))

    def train_model(self):
        print("Training ...")
        #:param training_type: The type of training to use to train the project
        #     (default: Regular). Possible values include: 'Regular', 'Advanced'
        iteration =self.trainer.train_project(self.project.id)
        while (iteration.status != "Completed"):
            iteration =self.trainer.get_iteration(self.project.id, iteration.id)
            print (iteration.status, '...')
            time.sleep(10)
        print ("Model trained!")
        print ("Iteration id: " + iteration.id)
        print ("Iteration name: " + iteration.name)

    def get_iteration_id(self):
        return self.trainer.get_iterations(self.project.id, raw=True).response.json()[0]['id']
    
    def get_iteration_publis_name(self):
        return self.trainer.get_iterations(self.project.id, raw=True).response.json()[0]['publishName']

    def get_untagged_imgs(self):
        return [i.id  for i in self.trainer.get_untagged_images(self.project.id)]