(:4. Which actors have starred in the most movies?:)

let $videos := doc("videos.xml")/result/videos/video
let $actors := doc("videos.xml")/result/actors/actor

let $max := max(
        for $actorRef in distinct-values($videos/actorRef)
        return count($videos/actorRef[. = $actorRef])
)
for $actorRef in distinct-values($videos/actorRef)
let $actor := $actors[@id = $actorRef]
let $count := count($videos/actorRef[. = $actorRef])
where $count = $max
return ($actor)