(:1. Which movies have the genre “special”?:)

for $video in doc("videos.xml")/result/videos/video
where $video/genre = "special"
return $video/title
