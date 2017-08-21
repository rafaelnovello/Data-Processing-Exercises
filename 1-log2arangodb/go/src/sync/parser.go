package main

import (
    "os"
    "fmt"
    "bufio"
    "strings"
    "io/ioutil"

    driver "github.com/arangodb/go-driver"
    "github.com/arangodb/go-driver/http"
)

func parse(line string) map[string]string {
    parsed := make(map[string]string)
    parsed["ip"] = strings.Split(line, " ")[0]
    date := strings.Split(line, "[")[1]
    parsed["date"] = strings.Split(date, "]")[0]
    method := strings.Split(line, "\"")[1]
    parsed["method"] = strings.Split(method, " ")[0]
    parsed["path"] = strings.Split(line, " ")[6]
    parsed["status"] = strings.Split(line, " ")[8]
    parsed["agent"] = strings.Split(line, "\"")[5]
    return parsed
}

func main() {
    conn, _ := http.NewConnection(http.ConnectionConfig{
        Endpoints: []string{"http://localhost:8529"},
    })
    client, _ := driver.NewClient(driver.ClientConfig{
        Connection: conn,
        Authentication: driver.BasicAuthentication("user", "pass"),
    })
    db, _ := client.Database(nil, "_system")

    col, _ := db.Collection(nil, "logs")

    path := "/path/to/logs/"
    files, _ := ioutil.ReadDir(path)
    for _, f := range files {
        fmt.Println(f.Name())
        file, _ := os.Open(path + f.Name())
        defer file.Close()

        scanner := bufio.NewScanner(file)
        var docs []map[string]string
        for scanner.Scan() {
            line := scanner.Text()
            parsed := parse(line)
            docs = append(docs, parsed)
            if len(docs) == 2000 {
                col.CreateDocuments(nil, docs)
                docs = nil
            }
        }
        if len(docs) > 0 {
            col.CreateDocuments(nil, docs)
        }
    }
}