from google.protobuf import field_mask_pb2
from google.proto.streetview.publish.v1 import resources_pb2
from google.streetview.publish.v1 import street_view_publish_service_client as client
from oauth2client.client import OAuth2WebServerFlow
from google.streetview.publish.v1 import enums
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from google.proto.streetview.publish.v1 import rpcmessages_pb2
import google.oauth2.credentials
import requests
import time

def get_access_token():
  client_id = 'CLIENT_ID'
  client_secret = 'CLIENT_SECRET'
  flow = OAuth2WebServerFlow(client_id=client_id,
                             client_secret=client_secret,
                             scope='https://www.googleapis.com/auth/streetviewpublish',
                             redirect_uri='http://localhost:8080/')
  storage = Storage('creds.data')

  # Open a web browser to ask the user for credentials.
  credentials = run_flow(flow, storage)
  assert credentials.access_token is not None
  return credentials.access_token
#End of get_access_token

def batchDelete():
	#function code
	photo_ids = ["PhotoId",
	"PhotoId"]

	delete_photo_response = streetview_client.batch_delete_photos(photo_ids)
	print("Delete response :" + str(delete_photo_response))
#End of batchDelete

def uploadPic(picRef):
	#function code
	upload_ref = streetview_client.start_upload()
	print("Created upload url: " + str(upload_ref))

	# Upload the photo bytes to the Upload URL.
	with open("/{destination}"+picRef+".jpg", "rb") as f:
	  print("Uploading file: " + f.name)
	  raw_data = f.read()
	  headers = {
	      "Authorization": "Bearer " + token,
	      "Content-Type": "image/jpeg",
	      "X-Goog-Upload-Protocol": "raw",
	      "X-Goog-Upload-Content-Length": str(len(raw_data)),
	  }
	  r = requests.post(upload_ref.upload_url, data=raw_data, headers=headers)
	  print("Upload response: " + str(r))

	photo = resources_pb2.Photo()
	photo.upload_reference.upload_url = upload_ref.upload_url
	create_photo_response = streetview_client.create_photo(photo)
	print("Create photo response: " + str(create_photo_response))
#End of uploadPic

def getListPhoto():
	view = enums.PhotoView.BASIC
	filter_ = ''
	photofromweb = streetview_client.list_photos(view,filter_)

	for element in photofromweb:
    	 print("PhotoID: " + str(element.photo_id) + "\n")
    	 print("ShareLink: " + str(element.share_link))
#End of uploadPic


def updatePhoto():
	picId = resources_pb2.PhotoId(id="PhotoId")
	connection2 = resources_pb2.Connection(target=picId)

	picIdMain = resources_pb2.PhotoId(id="PhotoId")
	photo = resources_pb2.Photo(photo_id=picIdMain,connections=[connection2])

	update_mask = field_mask_pb2.FieldMask()
	update_photo_request = rpcmessages_pb2.UpdatePhotoRequest(photo=photo, update_mask=update_mask)

	response = streetview_client.update_photo(photo=update_photo_request,options="NONE",update_mask=update_mask)



	pose = resources_pb2.Pose(level=resources_pb2.Level(name="lvl", number=0))
	connection1 = resources_pb2.Connection(target=resources_pb2.PhotoId(id="PhotoId"))
	connection2 = resources_pb2.Connection(target=resources_pb2.PhotoId(id="PhotoId"))
	photo = resources_pb2.Photo(connections=[connection1,connection2])

	update_mask = field_mask_pb2.FieldMask()
	response = streetview_client.batch_update_photos(photo)
	

	print("Update Response: " + str(response))

#End of UpdatePhoto
#END OF FUNCTIONS

token = get_access_token()
credentials = google.oauth2.credentials.Credentials(token)
# Create a client and request an Upload URL.
streetview_client = client.StreetViewPublishServiceClient(credentials=credentials)
#updatePhoto()
uploadPic("sample")
#batchDelete()
#uploadPic("level_1")
#getListPhoto()
#uploadPic("output_2")

