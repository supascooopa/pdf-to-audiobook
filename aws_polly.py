import boto3
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys


def calling_polly(text: str = "Hello World!"):
    # Create a client using the credentials and region defined
    polly = boto3.client(
        service_name="polly",
        region_name="us-west-1",
        aws_access_key_id=os.environ.get("ACCESS_KEY"),
        aws_secret_access_key=os.environ.get("SECRET_KEY")
    )

    try:
        # Request speech synthesis
        response = polly.synthesize_speech(Text=text, OutputFormat="mp3",
                                           VoiceId="Joanna")
    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        print(error)
        sys.exit(-1)

    # Access the audio stream from the response
    if "AudioStream" in response:
        # Note: Closing the stream is important because the service throttles on the
        # number of parallel connections. Here we are using contextlib.closing to
        # ensure the close method of the stream object will be called automatically
        # at the end of the with statement's scope.
        with closing(response["AudioStream"]) as stream:

            try:
                # Open a file for writing the output as a binary stream
                    polly_respnse = response['AudioStream'].read()
            except IOError as error:
                # Could not write to file, exit gracefully
                print(error)
                sys.exit(-1)

    else:
        # The response didn't contain audio data, exit gracefully
        print("Could not stream audio")
        sys.exit(-1)

    return polly_respnse
# print(calling_polly())