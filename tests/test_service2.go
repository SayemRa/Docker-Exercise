package main

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestInfoHandler(t *testing.T) {
	t.Run("ValidResponseStructure", func(t *testing.T) {
		req, _ := http.NewRequest("GET", "/info", nil)
		rr := httptest.NewRecorder()
		
		infoHandler(rr, req)
		
		if status := rr.Code; status != http.StatusOK {
			t.Errorf("Handler returned wrong status: got %v want %v", status, http.StatusOK)
		}

		var response SystemInfo
		if err := json.NewDecoder(rr.Body).Decode(&response); err != nil {
			t.Fatal("Failed to decode JSON response")
		}

		requiredFields := []string{
			"ip_address",
			"running_processes",
			"disk_space",
			"uptime",
			"memory_usage",
		}
		
		for _, field := range requiredFields {
			if value := reflect.ValueOf(response).FieldByName(strings.Title(field)); value.IsZero() {
				t.Errorf("Missing required field in response: %s", field)
			}
		}
	})
}