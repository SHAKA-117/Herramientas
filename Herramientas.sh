 #!/bin/bash

seleccion_distro(){
    echo "[ 1 ] Debian"
    echo "[ 2 ] Arch"
    echo " "
    read -p "Selecciona tu distro: " distro
    
    case $distro in
    	1)
    	    debian
    	    ;;
	2)
	    arch
	    ;;
    	*)
    	    echo "Opcion incorrecta"
    	    ;;
    esac
}
 
debian(){
 	 echo "[ 1 ]: Ranger     [ 7 ] Git           [ 13 ] Rofi PowerMenu      [ 19 ] Nodesjs y NPM"
 	 echo "[ 2 ]: Qtile      [ 8 ] Rust          [ 14 ] Rofi WifiMenu       [ 20 ] Conpilador"
	 echo "[ 3 ]: Rofi       [ 9 ] Cmake         [ 15 ] Docker              [ 21 ] Nushell" 
	 echo "[ 4 ]: Nitrogen   [ 10 ] Alacrytty    [ 16 ] Iconos de ranger    [ 22 ] Librerias para AudioVizualicer qtile"
	 echo "[ 5 ]: Fuentes    [ 11 ] Pulsemixer   [ 17 ] Oh my bash          [ 23 ] Unzip"
	 echo "[ 6 ]: Neovim     [ 12 ] Picom        [ 18 ] mysql"
	 echo " "
	 read -p "Selecciona una Opcion: "  herramienta
	
	 case $herramienta in
	     1)
		 apt-get install ranger
	         ;;
	     2)
		 apt install python3 python3-pip python3-venv python3-v-sim python-dbus-dev libpangocairo-1.0-0 python3-cairocffi libxkbcommon-dev libxkbcommon-x11-dev python3-pip
		 pip3 install qtile
		 ;;
	     3)
		 apt install rofi
		 ;;
	     4)
		 apt install nitrogen
		 ;;
	     5)
		 curl -O https://github.com/ryanoasis/nerd-fonts/releases/download/v3.4.0/Ubuntu.zip
		 curl -O https://github.com/ryanoasis/nerd-fonts/releases/download/v3.4.0/UbuntuMono.zip
		 unzip Ubuntu.zip -d Ubuntu
		 unzip UbuntuMono.zip -d UbuntuMono
		 mv Ubuntu/ /usr/share/fonts
		 mv UbuntuMono/ /usr/share/fonts
		 ;;
	     6)
		#agregar funcionalidad para detectar el tipo de arquitectura   uname -m
	      	 #Agregar esta linea al final de archivo .bashrc export PATH="$PATH:/opt/nvim-linux64/bin"
		 curl -LO https://github.com/neovim/neovim/releases/latest/download/nvim-linux-x86_64.tar.gz
		 sudo rm -rf /opt/nvim
		 sudo tar -C /opt -xzf nvim-linux-x86_64.tar.gz

	      	 sh -c 'curl -fLo "${XDG_DATA_HOME:-$HOME/.local/share}"/nvim/site/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
	      	 ;;
	      7)
	      	 apt-get install git
	      	 ;;
	      8)
	      	 curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
	      	 ;;
	      9)
	      	 apt install cmake g++ pkg-config libfreetype6-dev libfontconfig1-dev libxcb-xfixes0-dev libxkbcommon-dev python3
	      	 ;;
	      10)
	      	 git clone https://github.com/alacritty/alacritty.git
	      	 cd alacritty
	      	 rustup update stable
	      	 cargo build --release
	      	 #cargo build --release --no-default-features --features=wayland
	      	 #cargo build --release --no-default-features --features=x11
	      	 cp target/release/alacritty /usr/local/bin
	      	 cp extra/logo/alacritty-term.svg /usr/share/pixmaps/Alacritty.svg
	      	 desktop-file-install extra/linux/Alacritty.desktop
	      	 update-desktop-database

	     	#Agregar esta linea al final del archivo .bashrc export EDITOR=nvim
	     	;;
	      11)
	     	 apt-get install pulsemixer
	     	 ;;
	      12)
	     	 apt-get install picom
	     	 ;;
	      13)
	     	 cp rofi-power-menu ~/.local/bin/ 
	     	 ;;
	      14)
	     	 cp rofi-wifi-menu ~/.local/bin/
	     	 ;;
	      15)
	     	 ./InstallDocker.sh
	     	;;
	      16)
	     	 git clone https://github.com/alexanderjeurissen/ranger_devicons ~/.config/ranger/plugins/ranger_devicons
	     	 ranger --copy-config all 
	     	 echo "default_linemode devicons" >> $HOME/.config/ranger/rc.conf
	     	 ;;
	      17)
	     	 bash -c "$(curl -fsSL https://raw.githubusercontent.com/ohmybash/oh-my-bash/master/tools/install.sh)"
	     	 ;;
	      18)
	     	 #wget https://dev.mysql.com/get/mysql-apt-config_0.8.30-1_all.deb
	     	 #dpkg -i mysql-apt-config_0.8.30-1_all.deb
	     	 apt-get update
	     	 apt install mysql-server
	     	 ;;
	      19)
	     	 NODE_MAJOR=22
	     	 curl -sL https://deb.nodesource.com/setup_$NODE_MAJOR.x -o nodesource_setup.sh
	     	 bash nodesource_setup.sh
	     	 apt install nodejs
	     	 ;;
	      20)
	     	 apt install build-essential libssl-dev pkg-config
	     	 ;;
	      21)
	     	 git clone https://github.com/nushell/nushell.git
	     	 cd nushell
	     	 cargo build --release
	     	 sudo cp target/release/nu /usr/local/bin/
	     	 chsh -s $(which nu)
	     	 ;;
	      22)
	    	 sudo apt-get install portaudio19-dev
	    	 sudo pip3 install --break-system-packages pyaudio numpy
	    	 ;;
	     23)
		 apt-get install unzip 
		 ;;
	      *)
	     	 echo "!Opcion incorrecta!"
	     	 ;;
	   esac
}

seleccion_distro

