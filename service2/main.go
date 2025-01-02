package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os/exec"
	"runtime"
	"strings"
)

type SystemInfo struct {
	IPAddress       string `json:"ip_address"`
	RunningProcesses string `json:"running_processes"`
	DiskSpace       string `json:"disk_space"`
	Uptime          string `json:"uptime"`
	MemoryUsage     string `json:"memory_usage"`
}

func getSystemInfo() SystemInfo {
	// Get running processes
	processesCmd := exec.Command("ps", "-aux")
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

	// Get memory usage
	memCmd := exec.Command("free", "-h")
	memOutput, _ := memCmd.Output()
	memoryUsage := string(memOutput)

	return SystemInfo{
		IPAddress:       "127.0.0.1",
		RunningProcesses: runningProcesses,
		DiskSpace:       diskSpace,
		Uptime:          uptime,
		MemoryUsage:     memoryUsage,
	}
}

func infoHandler(w http.ResponseWriter, r *http.Request) {
	systemInfo := getSystemInfo()
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(systemInfo)
}

func main() {
	http.HandleFunc("/info", infoHandler)
	fmt.Println("Service2 running on port 8199...")
	http.ListenAndServe(":8199", nil)
}
