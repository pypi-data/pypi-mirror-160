# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tts_wrapper',
 'tts_wrapper.engines',
 'tts_wrapper.engines.google',
 'tts_wrapper.engines.microsoft',
 'tts_wrapper.engines.pico',
 'tts_wrapper.engines.polly',
 'tts_wrapper.engines.sapi',
 'tts_wrapper.engines.watson',
 'tts_wrapper.ssml']

package_data = \
{'': ['*']}

extras_require = \
{'google': ['google-cloud-texttospeech>=2.11.1,<3.0.0'],
 'microsoft': ['requests>=2.28.0,<3.0.0'],
 'polly': ['boto3>=1.24.34,<2.0.0'],
 'sapi': ['pyttsx3>=2.90,<3.0'],
 'watson': ['ibm-watson>=6.0.0,<7.0.0']}

setup_kwargs = {
    'name': 'tts-wrapper',
    'version': '0.8.0',
    'description': 'TTS-Wrapper makes it easier to use text-to-speech APIs by providing a unified and easy-to-use interface.',
    'long_description': '# TTS-Wrapper\n\n[![PyPI version](https://badge.fury.io/py/tts-wrapper.svg)](https://badge.fury.io/py/tts-wrapper)\n![build](https://github.com/mediatechlab/tts-wrapper/workflows/build/badge.svg)\n[![codecov](https://codecov.io/gh/mediatechlab/tts-wrapper/branch/master/graph/badge.svg?token=79IG7GAK0B)](https://codecov.io/gh/mediatechlab/tts-wrapper)\n[![Maintainability](https://api.codeclimate.com/v1/badges/b327dda20742c054bcf0/maintainability)](https://codeclimate.com/github/mediatechlab/tts-wrapper/maintainability)\n\n> ## **Contributions are welcome! Check our [contribution guide](./CONTRIBUTING.md).**\n\n_TTS-Wrapper_ makes it easier to use text-to-speech APIs by providing a unified and easy-to-use interface.\n\nCurrently the following services are supported:\n\n- AWS Polly\n- Google TTS\n- Microsoft TTS\n- IBM Watson\n- PicoTTS\n- SAPI (Microsoft Speech API)\n\n## Installation\n\nInstall using pip.\n\n```sh\npip install TTS-Wrapper\n```\n\n**Note: for each service you want to use, you have to install the required packages.**\n\nExample: to use `google` and `watson`:\n\n```sh\npip install TTS-Wrapper[google, watson]\n```\n\nFor PicoTTS you need to install the package on your machine. For Debian (Ubuntu and others) install the package `libttspico-utils` and for Arch (Manjaro and others) there is a package called `aur/pico-tts`.\n\n## Usage\n\nSimply instantiate an object from the desired service and call `synth()`.\n\n```Python\nfrom tts_wrapper import PollyTTS, PollyClient\n\ntts = PollyTTS(client=PollyClient())\ntts.synth(\'<speak>Hello, world!</speak>\', \'hello.wav\')\n```\n\nNotice that you must create a client object to work with your service. Each service uses different authorization techniques. Check out [the documentation](#authorization) to learn more.\n\n### Selecting a Voice\n\nYou can change the default voice and lang like this:\n\n```Python\nPollyTTS(voice=\'Camila\', lang=\'pt-BR\')\n```\n\nCheck out the list of available voices for [Polly](https://docs.aws.amazon.com/polly/latest/dg/voicelist.html), [Google](https://cloud.google.com/text-to-speech/docs/voices), [Microsoft](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/rest-text-to-speech#get-a-list-of-voices), and [Watson](https://cloud.ibm.com/docs/text-to-speech?topic=text-to-speech-voices).\n\n### SSML\n\nYou can also use [SSML](https://en.wikipedia.org/wiki/Speech_Synthesis_Markup_Language) markup to control the output of compatible engines.\n\n```Python\ntts.synth(\'<speak>Hello, <break time="3s"/> world!</speak>\', \'hello.wav\')\n```\n\nIt is recommended to use the `ssml` attribute that will create the correct boilerplate tags for each engine:\n\n```Python\ntts.synth(tts.ssml.add(\'Hello, <break time="3s"/> world!\'), \'hello.wav\')\n```\n\nLearn which tags are available for each service: [Polly](https://docs.aws.amazon.com/polly/latest/dg/supportedtags.html), [Google](https://cloud.google.com/text-to-speech/docs/ssml), [Microsoft](https://docs.microsoft.com/en-us/cortana/skills/speech-synthesis-markup-language), and [Watson](https://cloud.ibm.com/docs/text-to-speech?topic=text-to-speech-ssml).\n\n### Authorization\n\nTo setup credentials to access each engine, create the respective client.\n\n#### Polly\n\nIf you don\'t explicitly define credentials, `boto3` will try to find them in your system\'s credentials file or your environment variables. However, you can specify them with a tuple:\n\n```Python\nfrom tts_wrapper import PollyClient\nclient = PollyClient(credentials=(region, aws_key_id, aws_access_key))\n```\n\n#### Google\n\nPoint to your [Oauth 2.0 credentials file](https://developers.google.com/identity/protocols/OAuth2) path:\n\n```Python\nfrom tts_wrapper import GoogleClient\nclient = GoogleClient(credentials=\'path/to/creds.json\')\n```\n\n#### Microsoft\n\nJust provide your [subscription key](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/rest-text-to-speech#authentication), like so:\n\n```Python\nfrom tts_wrapper import MicrosoftClient\nclient = MicrosoftClient(credentials=\'TOKEN\')\n```\n\nIf your region is not the default "useast", you can change it like so:\n\n```Python\nclient = MicrosoftClient(credentials=\'TOKEN\', region=\'brazilsouth\')\n```\n\n#### Watson\n\nPass your [API key and URL](https://cloud.ibm.com/apidocs/text-to-speech/text-to-speech#authentication) to the initializer:\n\n```Python\nfrom tts_wrapper import WatsonClient\nclient = WatsonClient(credentials=(\'API_KEY\', \'API_URL\'))\n```\n\n#### PicoTTS & SAPI\n\nThese clients dont\'t require authorization since they run offline.\n\n```Python\nfrom tts_wrapper import PicoClient, SAPIClient\nclient = PicoClient()\n# or\nclient = SAPIClient()\n```\n\n## File Format\n\nBy default, all audio will be a wave file but you can change it to a mp3 using the `format` option:\n\n```Python\ntts.synth(\'<speak>Hello, world!</speak>\', \'hello.mp3\', format=\'mp3)\n```\n\n## License\n\nLicensed under the [MIT License](./LICENSE).\n',
    'author': 'Giulio Bottari',
    'author_email': 'giuliobottari@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mediatechlab/tts-wrapper',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
