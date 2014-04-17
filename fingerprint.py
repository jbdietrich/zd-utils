# Extract X509 certificate from SAML Response (b64 encoded or not)
# James Dietrich - https://github.com/jbdietrich

import re
import base64
import sys
import subprocess
import tempfile

certRegex = r'Certificate>(.*?)<'
beginText = "-----BEGIN CERTIFICATE-----\n"
endText = "-----END CERTIFICATE-----"

def extractCert(SAMLResponseFile):

	with open(SAMLResponseFile) as f:
		SAMLResponse = f.read()
		responseXML = base64.b64decode(SAMLResponse)

		if responseXML[0] == '<':
			return re.findall(certRegex, responseXML)[0]
		else:
			return re.findall(certRegex, SAMLResponse)[0]

def prettifyCert(rawX509):

	i = 0
	prettyString = ""
	totalLength = len(rawX509)

	for i in range(64, totalLength, 64):

		prettyString += rawX509[i-64:i] + "\n"
		diff = totalLength - i
		if diff < 64 and diff % 64 > 0:
			prettyString += rawX509[i:totalLength] + "\n"

	with tempfile.NamedTemporaryFile(delete=False) as f:
		f.write(beginText + prettyString + endText)
		return f.name

def findFingerprint(prettyCertFile):
	subprocess.call(["openssl", "x509","-noout", "-in",
		"{prettyCertFile}".format(prettyCertFile=prettyCertFile),
		"-fingerprint"])

if __name__ == "__main__":

	try:
		X509 = extractCert(sys.argv[1])
		prettyCertFile = prettifyCert(X509)
		findFingerprint(prettyCertFile)
	except IndexError:
		print "Please specify a filename to extract a fingerprint from.\n" \
					"usage: python fingerprint.py somefile"
