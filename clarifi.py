from clarifai.rest import ClarifaiApp
app = ClarifaiApp (api_key='de07e73879da40b4a65dee60367a0626')
model = app.models.get('travel-v1.0')
responce = model.predict_by_url('http://crisscrosstvl.com/wp-content/uploads/2016/05/sunset-plane.png')
print responce