const XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
const fs = require("fs");
const Path = require("path");
const Axios = require("axios");

const API_KEY = "";

const YOUTUBERS = [
  {
    username: "TrenBlack",
    id: "UCSSBvqWNPq_qO3_W4EJiOAA",
    uploadsId: "UUSSBvqWNPq_qO3_W4EJiOAA"
  }
];

class Scraper {
  constructor(uId, upId, username) {
    this.id = uId;
    this.upId = upId;
    this.username = username;

    this.videos = {
      viral: [],
      notViral: [],
      doesWell: []
    };
  }

  addStats() {
    const url = `https://www.googleapis.com/youtube/v3/channels?part=statistics&id=${this.id}&key=${API_KEY}`;

    const xhr = new XMLHttpRequest();

    xhr.open("GET", url, false);

    xhr.send();

    const data = JSON.parse(xhr.responseText);

    const stats = data.items[0].statistics;

    this.subs = parseInt(stats.subscriberCount, 10);
    this.totalViews = parseInt(stats.viewCount, 10);
    this.videoCount = parseInt(stats.videoCount, 10);
    this.averageViews = this.totalViews / this.videoCount;
  }

  calculateViewsScore(views) {
    return 0.5 * (views / this.averageViews) + 0.5 * (views / this.subs);
  }

  async getVideosList(token = "None", start = 0) {
    await this.createOutputFolders();

    const url =
      token === "None"
        ? `https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId=${this.upId}&key=${API_KEY}`
        : `https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId=${this.upId}&pageToken=${token}&key=${API_KEY}`;

    const xhr = new XMLHttpRequest();
    xhr.open("GET", url, false);
    xhr.send();

    const data = JSON.parse(xhr.responseText);

    if (data.nextPageToken) {
      token = data.nextPageToken;
    } else {
      token = "None";
    }

    const itemsLength = data.items.length;

    for (let i = 0; i < itemsLength; i++) {
      try {
        let category = "";
        const videoId = data.items[i].snippet.resourceId.videoId;
        const views = this.viewsFromId(videoId);
        const title = data.items[i].snippet.title;

        const thumbLink = data.items[i].snippet.thumbnails.default.url;
        const score = this.calculateViewsScore(parseInt(views, 10)).toFixed(2);

        console.log(i + start, "-", score);
        console.log(title);

        if (score < 1) {
          category = "not_viral";
          this.videos.notViral.push(title);
        } else if (score <= 2) {
          category = "does_well";
          this.videos.doesWell.push(title);
        } else {
          category = "viral";
          this.videos.viral.push(title);
        }

        await this.downloadThumbnail(
          thumbLink,
          category,
          `${this.username}-${i + start}`
        );
      } catch (err) {
        console.log(err);
        this.saveUserData();
      }
    }

    if (token !== "None") {
      return this.getVideosList(token, start + 50);
    }

    this.saveUserData();
  }

  viewsFromId(videoId) {
    const url = `https://www.googleapis.com/youtube/v3/videos?part=contentDetails,statistics&id=${videoId}&key=${API_KEY}`;

    const xhr = new XMLHttpRequest();
    xhr.open("GET", url, false);
    xhr.send();

    const data = JSON.parse(xhr.responseText);

    return data.items[0].statistics.viewCount;
  }

  saveUserData() {
    fs.writeFile(
      `./output/${this.username}.json`,
      JSON.stringify(this.videos, null, 2),
      err => {
        if (err) console.log(err);
        console.log("User data saved.");
      }
    );
  }

  async createOutputFolders() {
    fs.mkdir("./output/viral", { recursive: true }, err => {
      if (err) throw err;
    });
    fs.mkdir("./output/not_viral", { recursive: true }, err => {
      if (err) throw err;
    });
    fs.mkdir("./output/does_well", { recursive: true }, err => {
      if (err) throw err;
    });
  }

  async downloadThumbnail(url, category, name) {
    const path = Path.resolve(__dirname, `./output/${category}`, `${name}.jpg`);

    const response = await Axios({
      method: "GET",
      url: url,
      responseType: "stream"
    });

    response.data.pipe(fs.createWriteStream(path));

    return new Promise((resolve, reject) => {
      response.data.on("end", () => {
        resolve();
      });

      response.data.on("error", err => {
        reject(err);
      });
    });
  }
}

YOUTUBERS.forEach(youtuber => {
  const scraper = new Scraper(
    youtuber.id,
    youtuber.uploadsId,
    youtuber.username
  );

  scraper.addStats();
  scraper.getVideosList();
});
