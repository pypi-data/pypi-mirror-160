# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import subprocess

from distutils.spawn import find_executable
from os.path import join, isfile, expanduser
from ovos_utils.configuration import read_mycroft_config
from ovos_utils.xdg_utils import xdg_config_home

from ovos_plugin_manager.templates.tts import TTS, TTSValidator


class MimicTTSPlugin(TTS):
    """Interface to Mimic TTS."""

    def __init__(self, lang="en-us", config=None):
        config = config or {}
        super(MimicTTSPlugin, self).__init__(lang, config,
                                             MimicTTSValidator(self), 'wav')
        self.mimic_bin = find_executable("mimic")
        self.voice = self.voice or "ap"

    @staticmethod
    def find_premium_mimic():
        # HolmesV style
        xdg_mimic = join(xdg_config_home(), 'neon',
                         'voices', 'mimic_tn')
        if isfile(xdg_mimic):
            return xdg_mimic

        # HolmesV style default / once mycroft finally migrates to xdg
        xdg_mimic = join(xdg_config_home(), "mycroft",
                         'voices', 'mimic_tn')
        if isfile(xdg_mimic):
            return xdg_mimic

        # mycroft style data_dir
        config = read_mycroft_config() or {}
        if config.get("data_dir"):
            data_dir = expanduser(config['data_dir'])
            mimic_bin = join(data_dir, 'voices', 'mimic_tn')
            if isfile(mimic_bin):
                return mimic_bin

        # mycroft default location
        mimic_bin = "/opt/mycroft/voices/mimic_tn"
        if isfile(mimic_bin):
            return mimic_bin

    @staticmethod
    def modify_tag(tag):
        """Modify the SSML to suite Mimic."""
        ssml_conversions = {
            'x-slow': '0.4',
            'slow': '0.7',
            'medium': '1.0',
            'high': '1.3',
            'x-high': '1.6',
            'speed': 'rate'
        }
        for key, value in ssml_conversions.items():
            tag = tag.replace(key, value)
        return tag

    @staticmethod
    def parse_phonemes(phonemes):
        """Parse mimic phoneme string into a list of phone, duration pairs.

        Arguments
            phonemes (bytes): phoneme output from mimic
        Returns:
            (list) list of phoneme duration pairs
        """
        phon_str = phonemes.decode()
        pairs = phon_str.split(' ')
        return [pair.split(':') for pair in pairs if ':' in pair]

    def get_builtin_voices(self):
        return subprocess.check_output(
            [expanduser(self.mimic_bin), '-lv']).\
            decode("utf-8").split(":")[-1].strip().split(" ")

    def get_tts(self, sentence, wav_file, speaker=None):
        """Generate WAV and phonemes.

        Arguments:
            sentence (str): sentence to generate audio for
            wav_file (str): output file
            speaker (dict): override params for TTS voice
        Returns:
            tuple ((str) file location, (str) generated phonemes)
        """
        sentence = self.format_speak_tags(sentence, False)
        if not sentence:
            return wav_file, None

        args = [expanduser(self.mimic_bin), '-voice', self.voice,
                '-psdur', '-ssml']

        stretch = self.config.get('duration_stretch', None)
        if stretch:
            args += ['--setf', f'duration_stretch={stretch}']
        phonemes = subprocess.check_output(args + ['-o', wav_file,
                                                   '-t', sentence])

        return wav_file, self.parse_phonemes(phonemes)

    def viseme(self, phoneme_pairs):
        """Convert phoneme string to visemes.

        Arguments:
            phoneme_pairs (list): Phoneme output from mimic

        Returns:
            (list) list of tuples of viseme and duration
        """
        visemes = []
#        for phon, dur in phoneme_pairs:
#            visemes.append((VISIMES.get(phon, '4'), float(dur)))
        return visemes


class MimicTTSValidator(TTSValidator):
    def __init__(self, tts):
        super(MimicTTSValidator, self).__init__(tts)

    def validate_lang(self):
        lang = self.tts.lang.lower()
#        assert lang in self.get_lang_list()

    def validate_voice(self):
        if self.tts.voice is not None and \
                not self.tts.voice.startswith("http") and \
                not self.tts.voice.startswith("/"):
            assert self.tts.voice in self.tts.get_builtin_voices()

    def validate_connection(self):
        pass

    def get_tts_class(self):
        return MimicTTSPlugin

    @staticmethod
    def get_lang_list():
        return []
