class Chat {
    
    constructor(elem, allEmotes) {
        this.chat = elem;
        this.chatContainer = elem.parentElement;
        this.allEmotes = allEmotes;
        this.autoScroll = true;

        this.chatContainer.addEventListener("mouseenter", (event) => {
            this.autoScroll = false;
        });

        this.chatContainer.addEventListener("mouseleave", (event) => {
            this.autoScroll = true;
        });
    }

    addMessage(message) {
        const m2 = document.createElement("div");
        m2.setAttribute("class", "chat-message-container");

        const messageContainer = document.createElement("div");
        messageContainer.setAttribute("class", "chat-text-container");

        const date = new Date(Number(message["tags"]["tmi-sent-ts"]));
        const messageTime = document.createElement("span");
        messageTime.textContent = date.getHours().toString().padStart(2, "0") + ":" + date.getMinutes().toString().padStart(2, "0") + ":" + date.getSeconds().toString().padStart(2, "0");
        messageTime.setAttribute("class", "chat-message-ts");

        const messageUser = document.createElement("span");
        messageUser.textContent = message["tags"]["display-name"] + ":";
        messageUser.setAttribute("class", "chat-message-user");
        if (message["tags"]["color"] != "") {
            const color = tinycolor(message["tags"]["color"]);
            messageUser.setAttribute("style", "color: " + color.brighten(60).toHexString() + "; opacity: 0.6;")
        }

        var messageText = message["message"];
        var action = false;

        if (messageText.startsWith("\u0001ACTION")) {
            messageText = messageText.slice(8, messageText.length - 1);
            action = true;
        }

        var messageSplit = messageText.split(" ");
        var messageBuffer = [];
        var messageElements = [];

        for (const word of messageSplit) {
            var add = false;
            for (const [emote, url] of Object.entries(this.allEmotes)) {
                if (word == emote) {
                    if (messageBuffer.length > 0) {
                        const textSoFar = document.createElement("span");
                        textSoFar.textContent = messageBuffer.join(" ");
                        textSoFar.setAttribute("class", "message-text");
                        if (action) {
                            textSoFar.setAttribute("style", "font-style: italic;")
                        }
                        messageElements.push(textSoFar);
                    }

                    const emoteElement = document.createElement("img");
                    emoteElement.setAttribute("src", url);
                    emoteElement.setAttribute("class", "emote");

                    const emoteTooltip = document.createElement("span");
                    emoteTooltip.setAttribute("class", "emote-tooltiptext");
                    emoteTooltip.textContent = emote;

                    const tooltipElement = document.createElement("div");
                    tooltipElement.setAttribute("class", "emote-tooltip");
                    tooltipElement.appendChild(emoteElement);
                    tooltipElement.appendChild(emoteTooltip);

                    messageElements.push(tooltipElement);

                    add = true;
                    messageBuffer = [];
                    break;
                }
            }
            if (!add) {
                messageBuffer.push(word);
            }
        }

        const textSoFar = document.createElement("span");
        textSoFar.textContent = messageBuffer.join(" ");
        textSoFar.setAttribute("class", "message-text");
        if (action) {
            textSoFar.setAttribute("style", "font-style: italic;")
        }
        messageElements.push(textSoFar);
        
        messageContainer.appendChild(messageUser);
        for (const elem of messageElements) {
            messageContainer.appendChild(elem);
        }

        m2.appendChild(messageTime);
        m2.appendChild(messageContainer);

        this.chat.appendChild(m2);

        if (this.autoScroll) {
            this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
        }
    }
}
