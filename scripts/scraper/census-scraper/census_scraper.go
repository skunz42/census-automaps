package scraper

import (
	"encoding/json"
	"os"
)

func GetPopGroupCode(popGroup string, lookupPath string) string {
	// Return the population group code for a given group name

	// Get json contents
	jsonContents, err := os.ReadFile(lookupPath)
	if err != nil {
		panic(err)
	}

	// Unmarshall data into generic map
	var groupMapping map[string]interface{}
	if err := json.Unmarshal(jsonContents, &groupMapping); err != nil {
		panic(err)
	}

	// get code and assert as string
	groupCode := groupMapping[popGroup].(string)

	return groupCode
}
