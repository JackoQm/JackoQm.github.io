#!/bin/bash
usage() { 
	echo "quick_deploy [-acpdh] [commit comment]"
}
commit() { 
	git add . && git commit -m "$*" 
}
push() { 
	git push origin hexo 
}
deploy() { 
	hexo clean && hexo generate && hexo deploy 
}
case $# in
  1)
    case $1 in
        "-p") push
        ;;
        "-d") deploy
        ;;
        "-pd") push && deploy
        ;;
        *) usage
        ;;
    esac
  ;;
  2)
    case $1 in
        "-c") commit "$2"
        ;;
        "-cp") commit "$2" && push
        ;;
        "-a") commit "$2" && push && deploy
        ;;
        *) usage
        ;;
    esac
  ;;
  *)
  usage
  ;;
esac
