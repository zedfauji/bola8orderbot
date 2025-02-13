curl -X POST "https://graph.facebook.com/v17.0/608691765652135/messages" \
    -H "Authorization: Bearer EAAY1VhEDd4kBOyapwaYOPC9p4t3pv7p1NNBtKRflYojaf9xsfKUqYpiuKB2xpHMKBvi9nCDgLgER9cNJZB0Ha0QMrhJVUaSexQ7yLtbZCZCExuu45pHXyoqN070d7ZA9oqMH2wspHc1SEnmayzbkiBsZAvZChcWtyjABqV7AfpzFKIhXBC9GHvZCZAbZAaKJPXlxnCmST89uQ1og8XJZCh2Ux3IpRACwZDZD" \
    -H "Content-Type: application/json" \
    -d '{
        "messaging_product": "whatsapp",
        "to": "5213324940009",
        "type": "text",
        "text": { "body": "Test message from API" }
    }'
