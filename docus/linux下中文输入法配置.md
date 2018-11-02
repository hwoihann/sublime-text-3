## 1. SublimeText 3的安装
安装方式有多种，本文所描述的是从官方网站上下载64位的.deb文件 ，具体为http://c758482.r82.cf2.rackcdn.com/sublime-text_build-3059_amd64.deb文件，下载后双击即会自动使用默认的安装软件安装。

## 2. 相关依赖软件的安装
    sudo apt-get install build-essential libgtk2.0-dev

## 3. 拷贝如下代码到文件sublime_imfix.c文件中，该文件需要自己创建，随便放到那里都行。

```
/*
 * sublime-imfix.c
 * Use LD_PRELOAD to interpose some function to fix sublime input method support for linux.
 * By Cjacker Huang <jianzhong.huang at i-soft.com.cn> *
 *
 * gcc -shared -o libsublime-imfix.so sublime_imfix.c  `pkg-config --libs --cflags gtk+-2.0` -fPIC
 * LD_PRELOAD=./libsublime-imfix.so sublime_text
 */
#include <gtk/gtk.h>
#include <gdk/gdkx.h>

typedef GdkSegment GdkRegionBox;

struct _GdkRegion
{
    long size;
    long numRects;
    GdkRegionBox *rects;
    GdkRegionBox extents;
};

GtkIMContext *local_context;

void
gdk_region_get_clipbox (const GdkRegion *region,
                        GdkRectangle    *rectangle)
{
    g_return_if_fail (region != NULL);
    g_return_if_fail (rectangle != NULL);

    rectangle->x = region->extents.x1;
    rectangle->y = region->extents.y1;
    rectangle->width = region->extents.x2 - region->extents.x1;
    rectangle->height = region->extents.y2 - region->extents.y1;
    GdkRectangle rect;
    rect.x = rectangle->x;
    rect.y = rectangle->y;
    rect.width = 0;
    rect.height = rectangle->height;

    //The caret width is 2;
    //Maybe sometimes we will make a mistake, but for most of the time, it should be the caret.
    if (rectangle->width == 2 && GTK_IS_IM_CONTEXT(local_context)) {
        gtk_im_context_set_cursor_location(local_context, rectangle);
    }
}

//this is needed, for example, if you input something in file dialog and return back the edit area
//context will lost, so here we set it again.

static GdkFilterReturn event_filter (GdkXEvent *xevent, GdkEvent *event, gpointer im_context)
{
    XEvent *xev = (XEvent *)xevent;

    if (xev->type == KeyRelease && GTK_IS_IM_CONTEXT(im_context)) {
        GdkWindow *win = g_object_get_data(G_OBJECT(im_context), "window");

        if (GDK_IS_WINDOW(win)) {
            gtk_im_context_set_client_window(im_context, win);
        }
    }

    return GDK_FILTER_CONTINUE;
}

void gtk_im_context_set_client_window (GtkIMContext *context,
                                       GdkWindow    *window)
{
    GtkIMContextClass *klass;
    g_return_if_fail (GTK_IS_IM_CONTEXT (context));
    klass = GTK_IM_CONTEXT_GET_CLASS (context);

    if (klass->set_client_window) {
        klass->set_client_window (context, window);
    }

    if (!GDK_IS_WINDOW (window)) {
        return;
    }

    g_object_set_data(G_OBJECT(context), "window", window);
    int width = gdk_window_get_width(window);
    int height = gdk_window_get_height(window);

    if (width != 0 && height != 0) {
        gtk_im_context_focus_in(context);
        local_context = context;
    }

    gdk_window_add_filter (window, event_filter, context);
}

```
按照文件头上注释所说的编译该文件，在终端里进入到存放该文件的目录中，输入如下命令：
```
gcc -shared -o libsublime-imfix.so sublime_imfix.c  `pkg-config --libs --cflags gtk+-2.0` -fPIC
```

最后在当前目录下得到`libsublime-imfix.so`这个共享库。

## 4. 中文输入
到这里默认已经装好了中文输入法（搜狗输入法linux版）。  
得到第3步中的库libsublime-imfix.so之后，先试试看是否能正常使用中文输入法，在终端中输入如下命令：    
```
LD_PRELOAD=./libsublime-imfix.so subl             #subl是安装好SublimeText 3后的程序启动命令
```
如果一切正常，在启动之后，搜狗输入法就能可以输入了。
