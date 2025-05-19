#!/usr/bin/zsh
source $HOME/.zshrc
git clone https://github.com/zsh-users/zsh-autosuggestions.git $ZSH_CUSTOM/plugins/zsh-autosuggestions \
  && git clone https://github.com/zsh-users/zsh-syntax-highlighting.git $ZSH_CUSTOM/plugins/zsh-syntax-highlighting \
  && git clone https://github.com/zdharma-continuum/fast-syntax-highlighting.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/fast-syntax-highlighting \
  && omz plugin enable  zsh-autosuggestions zsh-syntax-highlighting fast-syntax-highlighting  debian pip uv python \
  && omz theme set duellj

sudo chown -R ${UID}:${GID} ${HOME} /workspaces

uv venv --prompt .venv 
uv sync

mkdir ${HOME}/.oh-my-zsh/completions
uv --generate-shell-completion zsh > ${HOME}/.oh-my-zsh/completions/_uv
uvx --generate-shell-completion zsh > ${HOME}/.oh-my-zsh/completions/_uvx
echo 'fpath=(~/.oh-my-zsh/completions $fpath)' >> ${HOME}/.zshrc
echo 'autoload -Uz compinit && compinit' >> ${HOME}/.zshrc
