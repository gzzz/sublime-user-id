import sublime, sublime_plugin

from binascii import unhexlify
from base64   import b64encode, b64decode
from struct   import pack, unpack


class Codec(object):
	def __init__(self, view):
		self.view = view

	def process(self, edit, command):
		view   = self.view
		method = getattr(self, command)

		for region in view.sel():
			if region.empty():
				region = sublime.Region(0, view.size())

			view.replace(edit, region, method(view.substr(region)))

	def decode(self, uid):
		return ''.join([format(i, 'X').zfill(8) for i in unpack('<LLLL', b64decode(uid))])

	def encode(self, uid):
		return b64encode(pack('<LLLL', *unpack('>LLLL', unhexlify(uid))))


class CodecCommand(sublime_plugin.TextCommand):
	def __init__(self, *args):
		super(CodecCommand, self).__init__(*args)

		self.codec = Codec(self.view)


class DecodeCommand(CodecCommand):
	def run(self, edit):
		self.codec.process(edit, 'decode')


class EncodeCommand(CodecCommand):
	def run(self, edit):
		self.codec.process(edit, 'encode')