# emailtobq
This is a simple code example that shows how to create a Google App Engine application that is able to receive emails, process them, extract the attachments and store them in the standard Google Cloud Storage bucket. This version does not include any type of controls, so the application will accept emails from any sender. The sample code also writes some logs in App Engine loggin sytem for tracing purposes. In order to make the application work, the google cloud storage python client library needs to be added to the deployment. Follow the instructions detailed here:

https://cloud.google.com/appengine/docs/standard/python/googlecloudstorageclient/setting-up-cloud-storage
