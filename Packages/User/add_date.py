import datetime, getpass
import sublime, sublime_plugin
import datetime

class AddDateTimeStampCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command("insert_snippet",
            {
                # "contents": "%s" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %A")
                # 可根据自己的需要进行调整（参照后面的日期时间格式）
                "contents": "/**""\n"
                " * ""\n"
                " * @author:      author""\n"
                " * @dateTime:    "  "%s"  %datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +"\n"
                " * @description: ""\n"
                " */"
            }
        )