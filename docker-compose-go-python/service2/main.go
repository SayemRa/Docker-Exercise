package main

import (
    "encoding/json"
    "fmt"
    "net"
    "net/http"
    "os/exec"
    "runtime"
    "strings"
)

// Data structure for the JSON response
type SystemInfo struct {
    IPAddress       string   `json:"ip_address"`
    RunningProcesses string   `json:"running_processes"`
    DiskSpace       string   `json:"disk_space"`
    Uptime          string   `json:"uptime"`
}

func getSystemInfo() SystemInfo {
    // Get IP address
    var ipAddress string
    interfaces, _ := net.Interfaces()
    for _, interf := range interfaces {
        addrs, _ := interf.Addrs()
        for _, addr := range addrs {
            var ip net.IP
            switch v := addr.(type) {
            case *net.IPNet:
                ip = v.IP
            case *net.IPAddr:
                ip = v.IP
            }
            if ip != nil && ip.To4() != nil {
                ipAddress = ip.String()
            }
        }
    }

    // Get running processes
    processesCmd := exec.Command("ps", "-ax")
    processesOutput, _ := processesCmd.Output()
    runningProcesses := string(processesOutput)

    // Get available disk space
    diskCmd := exec.Command("df", "-h")
    diskOutput, _ := diskCmd.Output()
    diskSpace := string(diskOutput)

    // Get uptime
    var uptime string
    if runtime.GOOS == "linux" {
        uptimeCmd := exec.Command("uptime", "-p")
        uptimeOutput, _ := uptimeCmd.Output()
        uptime = strings.TrimSpace(string(uptimeOutput))
    } else {
        uptime = "Not available"
    }

    // Package the data into the struct
    info := SystemInfo{
        IPAddress:       ipAddress,
        RunningProcesses: runningProcesses,
        DiskSpace:       diskSpace,
        Uptime:          uptime,
    }

    return info
}

func infoHandler(w http.ResponseWriter, r *http.Request) {
    // Get system information
    systemInfo := getSystemInfo()

    // Set content type to JSON
    w.Header().Set("Content-Type", "application/json")

    // Pretty print JSON response
    prettyJSON, err := json.MarshalIndent(systemInfo, "", "  ")  // Indent for pretty formatting
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    // Write the pretty printed JSON response
    w.Write(prettyJSON)
}


func main() {
    http.HandleFunc("/info", infoHandler)
    fmt.Println("Starting server on port 8199...")
    http.ListenAndServe(":8199", nil)
}
