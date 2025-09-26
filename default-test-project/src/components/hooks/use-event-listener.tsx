import * as React from "react"

type EventHandler<T extends EventTarget> = (event: Event) => void

export function useEventListener<T extends EventTarget>(
  eventName: string,
  handler: EventHandler<T>,
  element?: React.RefObject<T> | T | null,
  options?: AddEventListenerOptions
) {
  const savedHandler = React.useRef<EventHandler<T>>(handler)

  React.useEffect(() => {
    savedHandler.current = handler
  }, [handler])

  React.useEffect(() => {
    const targetElement = element?.current ?? element ?? window

    if (!(targetElement && targetElement.addEventListener)) {
      return
    }

    const eventListener: EventHandler<T> = (event) => savedHandler.current(event)

    targetElement.addEventListener(eventName, eventListener as EventListener, options)

    return () => {
      targetElement.removeEventListener(eventName, eventListener as EventListener, options)
    }
  }, [eventName, element, options])
}