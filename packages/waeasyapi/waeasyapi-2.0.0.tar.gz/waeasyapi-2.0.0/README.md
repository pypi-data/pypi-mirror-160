# WA Easy API Python Client

[![PyPI](https://img.shields.io/pypi/pyversions/waeasyapi.svg)]() [![License](https://img.shields.io/:license-mit-blue.svg)](https://opensource.org/licenses/MIT)

Python bindings for interacting with the WA Easy API

WA Easy API allows you to send and receive messages using Official WhatsApp APIs.

This is primarily meant for developers who wish to perform interactions with the WA Easy API programatically.

## Installation

```sh
$ pip install waeasyapi
```

## Usage

You need to setup your key and secret using the following:
You can find your keys at <https://waeasyapi.com/>.

```py
import waeasyapi
client = waeasyapi.Client(auth=("<YOUR_ACC_ID>", "<YOUR_ACC_SECRET>"))
```

## Usage - Messaging

```py
# number must start with the country's dialing code

# example - For USA: 158883993
# example - For India: 919876543210

# example - send a text message
client.message.sendTextMessage({
  "number" : "188377783",
  "message" : "Hello world!"
})

# example - send an approved WhatsApp template
client.message.sendTemplateMessage({
  "number" : "188377783",
  "template" : "template-name",
  "params" : { 
    "key1" : "value1",
    "key2" : "value2"
  }
})

# example - send an image message
client.message.sendImageMessage({
  "number" : "188377783",
  "params" : { 
    "link" : "your_image_link"
  }
})

# example - send a video message
client.message.sendVideoMessage({
  "number" : "188377783",
  "params" : { 
    "link" : "your_video_link"
  }
})

# example - send an audio message
client.message.sendAudioMessage({
  "number" : "188377783",
  "params" : { 
    "link" : "your_audio_link"
  }
})

# example - send a voice message
client.message.sendVoiceMessage({
  "number" : "188377783",
  "params" : { 
    "link" : "your_voice_link"
  }
})

# example - send url message
client.message.sendURLMessage({
  "number" : "188377783",
  "url" : "https://example.com"
})

```

## Usage - Template

```py

# eg - create and submit a WhatsApp template message
client.template.createTemplate({
  "name": "template_name",
  "category": "OTP",
  "language": "en",
  "components": [
    { "type": "HEADER", "format": "TEXT", "text": "I am header." },  # format = TEXT | IMAGE | VIDEO | DOCUMENT
    { "type": "BODY", "text": "I am body." },
    { "type": "FOOTER", "text": "I am footer." },
    { 
      "type": "BUTTONS", 
      "buttons": [ # for quick reply buttons, type = QUICK_REPLY
        { "type": "PHONE_NUMBER", "text": "Call Us", "phone_number": "+18887777877" },
        { "type": "URL", "text": "Visit Website", "url": "https://waeasyapi.com" },
      ]
    },
  ]
});

# get all templates
client.template.getTemplates();

# templateName = name_of_the_template
client.template.deleteTemplate(templateName);

```

## Usage - Profile

```py
# manage your WhatsApp Business Profile

# example - get your WhatsApp profile photo
client.profile.getProfilePhoto();

# example - get your WhatsApp profile about
client.profile.getProfileAbout();

# example - get your WhatsApp business profile
client.profile.getBusinessProfile();

# example - delete your WhatsApp business photo
client.profile.deleteProfilePhoto();

# example - change your WhatsApp business photo
client.profile.changeProfilePhoto({
  "photo": "base64_string_of_image"
});

# example - change your WhatsApp profile about
client.profile.changeProfileAbout({
  "about": "Hey! I\'m using WA Easy API!"
});

# example - change your WhatsApp business profile
client.profile.changeBusinessProfile({
  "description": 'Official WhatsApp Business APIs & Messaging Platform',
  "vertical": 'Professional Services',
  "address": 'California, USA',
  "email": 'team@waeasyapi.com',
  "websites": ['https://waeasyapi.com']
});

# acceptable business verticals are
# const verticals = [
#   'Automotive',
#   'Beauty, Spa and Salon',
#   'Clothing and Apparel',
#   'Education',
#   'Entertainment',
#   'Event Planning and Service',
#   'Finance and Banking',
#   'Food and Grocery',
#   'Public Service',
#   'Hotel and Lodging',
#   'Medical and Health',
#   'Non-profit',
#   'Professional Services',
#   'Shopping and Retail',
#   'Travel and Transportation',
#   'Restaurant',
#   'Other'
# ]

```

## Usage - Media

```py

# eg - get your uploaded media
client.media.getMedia(mediaId);

# eg - upload your media
# send a post (`multipart/form-data`) request with the media on `file` key to
# basic auth is acceptable with acc_id as username & acc_secret as password
https://api.waeasyapi.com/v1/media/upload

# acceptable content types

# audio - audio/aac, audio/mp4, audio/amr, audio/mpeg, audio/ogg; codecs=opus 
# Note: The base audio/ogg type is not supported.

# document - Any valid MIME-type.

# image - image/jpeg, image/png

# sticker - image/webp

# video - video/mp4, video/3gpp
# Note: Only H.264 video codec and AAC audio codec is supported. 
# Note: Only videos with a single audio stream are supported.

```

## App Details

After setting up client, you can set your app details before making any request
to WA Easy API using the following:

```py
client.set_app_details({"title" : "<YOUR_APP_TITLE>", "version" : "<YOUR_APP_VERSION>"})
```

For example, you can set the title to `Django` and version to `1.8.17`. Please ensure
that both app title and version are strings.

## Bugs? Feature requests? Pull requests?

All of those are welcome. You can [file issues][issues] or [submit pull requests][pulls] in this repository.

[issues]: https://github.com/waeasyapi/waeasyapi-python/issues
[pulls]: https://github.com/waeasyapi/waeasyapi-python/pulls
