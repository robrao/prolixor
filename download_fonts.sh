echo "Create directory for fonts..."
mkdir -p fonts && cd fonts

echo "Downloading fonts..."
wget --progress=bar https://github.com/google/fonts/archive/master.zip 

echo "Unzipping fonts"
unzip master.zip -d .

# If need to install on system
#unameOut="$(uname -s)"
#case "${unameOut}" in
    #Linux*)     machine=Linux;;
    #Darwin*)    machine=Mac;;
    #CYGWIN*)    machine=Cygwin;;
    #MINGW*)     machine=MinGw;;
    #*)          machine="UNKNOWN:${unameOut}"
#esac

#echo "Install fonts"
#if [$unameOut == Linux"]; then
    #cp *.ttf /usr/local/share/fonts
#else
    #cp *.ttf /Library/Fonts/
#fi

echo "Done."
