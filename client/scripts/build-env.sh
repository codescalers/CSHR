#!/bin/sh

#!/bin/sh
set -ex
values="
window.env = {
  CSHR_API: '$CSHR_API',
};
"
# decide the config file path
file="/usr/share/nginx/html/config.js"
echo $values > $file
echo -e "\e[1;32m$values"

echo "++++++++++++++++++++++++++++++++++++++++++++"
echo "file=$file"
echo "++++++++++++++++++++++++++++++++++++++++++++"
