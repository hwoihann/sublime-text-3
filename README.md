# sublime-text-3
backup~

```sh
cp ~/.config/sublime-text-3/Installed\ Packages/ ./ -r
cp ~/.config/sublime-text-3/Local ./ -r
cp ~/.config/sublime-text-3/Packages/ ./ -r 
```


Sublime Text 的 data 文件夹路径如下：

 - OS X: ~/Library/Application Support/Sublime Text 3
 - Windows: %APPDATA%\Sublime Text 3
 - Linux: ~/.config/sublime-text-3

```
import urllib.request,os; pf = 'Package Control.sublime-package'; ipp = sublime.installed_packages_path(); urllib.request.install_opener( urllib.request.build_opener( urllib.request.ProxyHandler()) ); open(os.path.join(ipp, pf), 'wb').write(urllib.request.urlopen( 'http://sublime.wbond.net/' + pf.replace(' ','%20')).read())
```
