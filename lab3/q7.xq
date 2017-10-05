(:7. Who have starred in the most distinct types of genre?:)

let $videos := doc("videos.xml")/result/videos/video
let $actors := doc("videos.xml")/result/actors

let $most_genres :=
    for $actorid in $actors/actor/@id
    order by count($videos[actorRef = $actorid]/genre) descending
    return distinct-values($actors/actor[@id = $actorid])
return concat('actor="', $most_genres[1], '"')
