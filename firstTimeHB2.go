package main

import (
	"fmt"
	"net/http"
	"os"
	"strings"
	"time"

	"golang.org/x/net/html"
)

func getText(n *html.Node) string {
	if n.Type == html.TextNode {
		return n.Data
	}
	var text string
	for c := n.FirstChild; c != nil; c = c.NextSibling {
		text += getText(c)
	}
	return strings.TrimSpace(text)
}

func main() {
	start := time.Now()

	resp, err := http.Get("https://www.fairfaxcounty.gov/housing/homeownership/FirstTimeHomebuyers")
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	doc, err := html.Parse(resp.Body)
	if err != nil {
		panic(err)
	}

	var links []string
	var f func(*html.Node)
	f = func(n *html.Node) {
		if n.Type == html.ElementNode && n.Data == "h2" {
			links = append(links, getText(n))
		}
		for c := n.FirstChild; c != nil; c = c.NextSibling {
			f(c)
		}
	}
	f(doc)

	listingDate := time.Now()
	dateAnnounced := listingDate.Format("01/02/06")

	fname := "output.txt"
	existing, err := os.ReadFile(fname)
	if err != nil {
		// file not found, create new
		file, err := os.Create(fname)
		if err != nil {
			panic(err)
		}
		defer file.Close()
		for _, text := range links {
			fmt.Println(text)
			file.WriteString(text + "\n")
		}
	} else {
		existingStr := string(existing)
		file, err := os.OpenFile(fname, os.O_RDWR|os.O_APPEND, 0666)
		if err != nil {
			panic(err)
		}
		defer file.Close()
		for _, text := range links {
			if !strings.Contains(existingStr, text) {
				fmt.Println(text)
				file.WriteString(text + " | " + dateAnnounced + "\n")
			}
		}
	}

	elapsed := time.Since(start)
	fmt.Printf("Execution time: %v\n", elapsed)
}
