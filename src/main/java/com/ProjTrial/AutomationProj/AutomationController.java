package com.ProjTrial.AutomationProj;

import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

import java.io.*;

@RestController
@RequestMapping("/api")
public class AutomationController
{

    Process duplicateProcess;
    Process backupProcess;
    Process monitorProcess;
    Process tempProcess;


    String python()
    {
        String os = System.getProperty("os.name").toLowerCase();

        if(os.contains("win")){
            return "python";
        }
        else{
            return "python3";
        }
    }

    // =====================================================
    // DUPLICATE CLEANER
    // =====================================================

    @GetMapping("/duplicate")
    public SseEmitter runDuplicate(@RequestParam String path)
    {

        String[] cmd = {python(),"python/disk_sanitizer.py",path};

        return runScript(cmd,"duplicate");

    }


    // =====================================================
    // BACKUP AUTOMATION
    // =====================================================

    @GetMapping("/backup")
    public SseEmitter runBackup(
            @RequestParam String interval,
            @RequestParam String source){

        String[] cmd = {python(),"python/data_shield.py",interval,source};

        return runScript(cmd,"backup");

    }


    // =====================================================
    // PROCESS SURVEILLANCE
    // =====================================================

    @GetMapping("/monitor")
    public SseEmitter runMonitor(
            @RequestParam String interval,
            @RequestParam String folder)
    {

        String[] cmd = {python(),"python/process_surveillance.py",interval,folder};

        return runScript(cmd,"monitor");

    }


    // =====================================================
    // TEMP FILE CLEANER
    // =====================================================

    @GetMapping("/tempclean")
    public SseEmitter runTemp(@RequestParam String path)
    {

        String[] cmd = {python(),"python/temp_file_cleaner.py",path};

        return runScript(cmd,"temp");

    }


    // =====================================================
    // STOP FUNCTIONS
    // =====================================================

    @PostMapping("/stop/duplicate")
    public void stopDuplicate()
    {

        if(duplicateProcess != null)
        {
            duplicateProcess.destroyForcibly();
        }

    }

    @PostMapping("/stop/backup")
    public void stopBackup()
    {

        if(backupProcess != null)
        {
            backupProcess.destroyForcibly();
        }

    }

    @PostMapping("/stop/monitor")
    public void stopMonitor()
    {

        if(monitorProcess != null)
        {
            monitorProcess.destroyForcibly();
        }

    }

    @PostMapping("/stop/tempclean")
    public void stopTemp()
    {

        if(tempProcess != null)
        {
            tempProcess.destroyForcibly();
        }

    }


    // =====================================================
    // SCRIPT RUNNER
    // =====================================================

    public SseEmitter runScript(String[] command,String type)
    {

        SseEmitter emitter = new SseEmitter();

        new Thread(() -> {

            try{

                ProcessBuilder pb = new ProcessBuilder(command);

                pb.redirectErrorStream(true);

                Process process = pb.start();

                if(type.equals("duplicate")){
                    duplicateProcess = process;
                }
                else if(type.equals("backup")){
                    backupProcess = process;
                }
                else if(type.equals("monitor")){
                    monitorProcess = process;
                }
                else if(type.equals("temp")){
                    tempProcess = process;
                }

                BufferedReader reader =
                        new BufferedReader(
                                new InputStreamReader(process.getInputStream())
                        );

                String line;

                while((line = reader.readLine()) != null){

                    emitter.send(line);

                }

                emitter.complete();

            }
            catch(Exception e)
            {

                try{
                    emitter.send("ERROR : " + e.getMessage());
                }
                catch(Exception ignored){}

                emitter.complete();

            }

        }).start();

        return emitter;

    }

}