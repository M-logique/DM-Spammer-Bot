package main

/*
#include <stdlib.h>
*/
import "C"

import (
	"bufio"
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"math/rand"
	"net/http"
	"os"
	"strings"
	"sync"
	"time"
)

type Tools struct {
	Token string
}

type CreateDMRequest struct {
	RecipientID string `json:"recipient_id"`
}

type CreateDMResponse struct {
	ID string `json:"id"`
}

func (t *Tools) api(endpoint string) string {
	baseURL := "https://discord.com/api/v9"
	return baseURL + endpoint
}

func (t *Tools) sendMessageEmbed(channelID string, message string, content string) (bool, error) {
	url := t.api(fmt.Sprintf("/channels/%s/messages", channelID))
	fmt.Println(url)

	embed := map[string]interface{}{
		"description": message,
	}

	payload := map[string]interface{}{
		"content": content,
		"embeds":  []map[string]interface{}{embed},
	}

	jsonData, err := json.Marshal(payload)
	if err != nil {
		return false, err
	}

	req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
	if err != nil {
		return false, err
	}
	req.Header.Set("Authorization", "Bot "+t.Token)
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return false, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := ioutil.ReadAll(resp.Body)
		return false, fmt.Errorf("failed to send message, status code: %d, response: %s", resp.StatusCode, string(body))
	}

	return true, nil
}

func (t *Tools) sendMessage(channelID, message string) (bool, error) {
	url := t.api(fmt.Sprintf("/channels/%s/messages", channelID))
	payload := map[string]string{"content": message}
	jsonData, err := json.Marshal(payload)
	if err != nil {
		return false, err
	}

	req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
	if err != nil {
		return false, err
	}
	req.Header.Set("Authorization", "Bot "+t.Token)
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return false, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		return false, fmt.Errorf("failed to send message, status code: %d", resp.StatusCode)
	}

	return true, nil
}

func (t *Tools) createDMAndSendMessage(userID, message string) (bool, error) {
	url := t.api("/users/@me/channels")
	payload := CreateDMRequest{RecipientID: userID}
	jsonData, err := json.Marshal(payload)
	if err != nil {
		return false, err
	}

	req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
	if err != nil {
		return false, err
	}
	req.Header.Set("Authorization", "Bot "+t.Token)
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return false, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		return false, fmt.Errorf("failed to create DM, status code: %d", resp.StatusCode)
	}

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return false, err
	}

	var dmResponse CreateDMResponse
	if err := json.Unmarshal(body, &dmResponse); err != nil {
		return false, err
	}

	return t.sendMessage(dmResponse.ID, message)
}

func readTokens() ([]string, error) {
	file, err := os.Open("./data/tokens.txt")
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var lines []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	if err := scanner.Err(); err != nil {
		return nil, err
	}

	return lines, nil
}

//export SendDirectMessages
func SendDirectMessages(userID *C.char, message *C.char) {
	goUserID := C.GoString(userID)
	goMessage := C.GoString(message)

	tokens, err := readTokens()
	if err != nil {
		fmt.Println("There was an error reading tokens:", err)
		return
	}

	var wg sync.WaitGroup
	for _, token := range tokens {
		wg.Add(1)
		go func(t string) {
			defer wg.Done()
			tools := &Tools{Token: t}
			_, err := tools.createDMAndSendMessage(goUserID, goMessage)
			if err != nil {
				fmt.Printf("There was an error sending dm to %s with the token %s: %s\n", goUserID, t, err)
			}

		}(token)
	}
	wg.Wait()
}

func randomChannelID(channelIDs string) string {

	splitChannels := strings.Split(channelIDs, ",")
	
	rand.Seed(time.Now().UnixNano())

	randomIndex := rand.Intn(len(splitChannels))

	return splitChannels[randomIndex]
}

//export SendChannelMessages
func SendChannelMessages(channelIDs *C.char, message *C.char, content *C.char) {
	goChannelIDs := C.GoString(channelIDs)
	goMessage := C.GoString(message)
	goContent := C.GoString(content)
	tokens, err := readTokens()
	if err != nil {
		fmt.Println("There was an error reading tokens:", err)
		return
	}

	var wg sync.WaitGroup
	for _, token := range tokens {
		wg.Add(1)
		go func(t string) {
			defer wg.Done()
			tools := &Tools{Token: t}
			randomChannel := randomChannelID(goChannelIDs)
			_, err := tools.sendMessageEmbed(randomChannel, goMessage, goContent)
			if err != nil {
				fmt.Printf("There was an error sending message to %s with the token %s: %s\n", randomChannel, t, err)
			}

		}(token)
	}
	wg.Wait()
}

func main() {}
