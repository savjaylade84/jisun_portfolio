
# removing requirement file
echo "[Task]: [ Removing the existing requirement file ]"
rm -f requirements.txt
echo "[Task]: [ Done ]"

# creating and listing the packages
echo "[Task]: [ Creating file and listing the packages ]" 
pip freeze > requirements.txt
echo "[Task]: [ Done ]"
