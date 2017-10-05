(:2. Which director has directed at least two movies, and which movies has he directed? :)

let $video := doc("videos.xml")/result/videos/video
for $director in distinct-values($video/director)
let $directors_titles := $video[director = $director]/title
where count($video/director[. = $director]) >= 2

return <movie director="{$director}">{$directors_titles}</movie>

(:let $nl := "&#10;":)
(:return concat($nl,' ', ):)