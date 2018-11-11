rmdir skill_env_package --ignore-fail-on-non-empty
mkdir skill_env_package
pip install -r py/requirements.txt -t skill_env_package
cp -r lambda/py/* skill_env_package/

# zip everything 
rm skill_env_package.zip

cd skill_env_package
zip -r skill_env_package.zip *

mv skill_env_package.zip ../skill_env_package.zip

cd ..
