#!/bin/bash
openssl req -x509 -out devops-assignment.inspectorio.info.crt -keyout devops-assignment.inspectorio.info.key \
-newkey rsa:2048 -nodes -sha256 \
-subj '/CN=devops-assignment.inspectorio.info' -extensions EXT -config <( \
 printf "[dn]\nCN=devops-assignment.inspectorio.info\n[req]\ndistinguished_name = dn\n[EXT]\nsubjectAltName=DNS:devops-assignment.inspectorio.info\nkeyUsage=digitalSignature\nextendedKeyUsage=serverAuth")