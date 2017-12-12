# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START log_sender_handler]
import logging
import os
import cloudstorage as gcs
import webapp2

from google.appengine.api import app_identity
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler


class LogSenderHandler(InboundMailHandler):
    def receive(self, mail_message):
        logging.info("Received a message from: " + mail_message.sender)
        logging.info("With subject: " + mail_message.subject)
# [END log_sender_handler]
# [START bodies]
        plaintext_bodies = mail_message.bodies('text/plain')
        html_bodies = mail_message.bodies('text/html')

        for content_type, body in html_bodies:
            decoded_html = body.decode()
            # ...
# [END bodies]
            logging.info("Html body of length %d.", len(decoded_html))
        for content_type, body in plaintext_bodies:
            plaintext = body.decode()
            logging.info("Plain text body of length %d.", len(plaintext))
# [START attachments]
        bucket_name = os.environ.get('BUCKET_NAME', app_identity.get_default_gcs_bucket_name())
        logging.info("Attachments will be written to bucket " + bucket_name)
        for attach in mail_message.attachments:
            filename = attach[0]
            contents = attach[1]
            logging.info("Attachmend found: " + filename)
            # [START write to the bucket]
            write_retry_params = gcs.RetryParams(backoff_factor=1.1)
            gcs_file = gcs.open("/" + bucket_name + "/" + filename, 'w', content_type='text/plain', options={'x-goog-meta-foo': 'foo','x-goog-meta-bar': 'bar'}, retry_params=write_retry_params)
            gcs_file.write(contents.decode().encode('utf-8'))
            gcs_file.close()                     
            # [END write to the bucket]
# [END attachments]

# [START app]
app = webapp2.WSGIApplication([LogSenderHandler.mapping()], debug=True)
# [END app]
