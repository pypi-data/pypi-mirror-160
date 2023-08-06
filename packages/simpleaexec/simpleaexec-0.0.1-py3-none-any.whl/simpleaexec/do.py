import io
import contextlib
from aioconsole import aexec

async def asyncexecute(code):
	if code is not None:
		code = code.replace("~", "	")
		str_obj = io.StringIO()
		try:
			with contextlib.redirect_stdout(str_obj):
				await aexec(code)
		except Exception as e:
			return f"{e.__class__.__name__}: {e}"
		if not str_obj.getvalue():
			return 'Done!'
		else:
			return str_obj.getvalue()
	else:
		return 'No arguments?'