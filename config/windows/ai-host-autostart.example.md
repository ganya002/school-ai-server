# Autostart for the inference engine (Windows 11 example)

Both nodes stay on Windows 11. Use a **Windows service** or **Task Scheduler**, not systemd.

Do not apply this on a live PC without Gabby's OK. Keep listen addresses on `127.0.0.1` unless the interconnect plan says otherwise. The model is TBD.

## Option A: the engine's own Windows service

Ollama for Windows typically installs a user or system service. Confirm it starts at sign-in or at boot, and that it comes back after a crash.

```powershell
Get-Service *ollama*
# Start-Service <name>    # only with approval
```

## Option B: Task Scheduler (generic)

Create a task that runs the engine's Windows binary at startup, as a dedicated service account if one was created, with highest privileges only if required, and restart-on-failure.

```powershell
# EXAMPLE — placeholders only, do not run as-is
$action = New-ScheduledTaskAction -Execute "C:\PATH\TO\llama-server.exe" -Argument "--host 127.0.0.1 --port PORT --model C:\AI\models\MODEL_FILE"
$trigger = New-ScheduledTaskTrigger -AtStartup
$settings = New-ScheduledTaskSettingsSet -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1) -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
# Register-ScheduledTask -TaskName "AI-llama-server" -Action $action -Trigger $trigger -Settings $settings
```

If the signed-in user is not always logged on, prefer a system service or a task running whether the user is logged on or not, and keep the Windows power plan from sleeping (see docs/os-installation.md).

WSL2 or Docker Desktop compose files are not the default and need Gabby's OK first.
