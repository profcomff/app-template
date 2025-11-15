import React, { useEffect, useState } from "react";
import axios from 'axios';
import { Button, IconButton, Input, Popover, PopoverContent, PopoverHandler } from "@material-tailwind/react";
import { ArrowRightIcon, ArrowLeftIcon, ChevronLeftIcon, ChevronRightIcon } from "@heroicons/react/24/outline";
import { format } from "date-fns";

import { CardDefault } from "../EventCard";
import { DayPicker } from "react-day-picker";

const EventsSection = () => {
    const [events, setEvents] = useState([])
    const [active, setActive] = React.useState(1);
    const [date, setDate] = useState();


    const getItemProps = (index) =>
    ({
        variant: active === index ? "filled" : "text",
        color: "gray",
        onClick: () => setActive(index),
    });

    const next = () => {
        if (active === 5) return;

        setActive(active + 1);
    };

    const prev = () => {
        if (active === 1) return;

        setActive(active - 1);
    };

    useEffect(() => {
        axios.get("http://79.174.91.168/posts", {
            headers: {
                'Authorization': 'eBqaCuBSlrIpCpFESwwGfSXndwhqAicpsOOgJlDxTWSGypBgLUwEdUwTQaaXVJDY'
            }
        }).then(({ data }) => setEvents(data))
    }, [])
    return (
        <div className="mx-auto max-w-screen-xl px-6 py-3">
            <h3>Select by date:</h3>
            <div className="py-6 w-72">
                <Popover placement={`${window.innerWidth < 768 ? 'bottom' : 'right'}`}>
                    <PopoverHandler>
                        <Input
                            label="Select a Date"
                            onChange={() => null}
                            value={date ? format(date, "PPP") : ""}
                        />
                    </PopoverHandler>
                    <PopoverContent>
                        <DayPicker
                            mode="single"
                            selected={date}
                            onSelect={setDate}
                            showOutsideDays
                            className="border-0"
                            classNames={{
                                caption: "flex justify-center py-2 mb-4 relative items-center",
                                caption_label: "text-sm font-medium text-gray-900",
                                nav: "flex items-center",
                                nav_button:
                                    "h-6 w-6 bg-transparent hover:bg-blue-gray-50 p-1 rounded-md transition-colors duration-300",
                                nav_button_previous: "absolute left-1.5",
                                nav_button_next: "absolute right-1.5",
                                table: "w-full border-collapse",
                                head_row: "flex font-medium text-gray-900",
                                head_cell: "m-0.5 w-9 font-normal text-sm",
                                row: "flex w-full mt-2",
                                cell: "text-gray-600 rounded-md h-9 w-9 text-center text-sm p-0 m-0.5 relative [&:has([aria-selected].day-range-end)]:rounded-r-md [&:has([aria-selected].day-outside)]:bg-gray-900/20 [&:has([aria-selected].day-outside)]:text-white [&:has([aria-selected])]:bg-gray-900/50 first:[&:has([aria-selected])]:rounded-l-md last:[&:has([aria-selected])]:rounded-r-md focus-within:relative focus-within:z-20",
                                day: "h-9 w-9 p-0 font-normal",
                                day_range_end: "day-range-end",
                                day_selected:
                                    "rounded-md bg-gray-900 text-white hover:bg-gray-900 hover:text-white focus:bg-gray-900 focus:text-white",
                                day_today: "rounded-md bg-gray-200 text-gray-900",
                                day_outside:
                                    "day-outside text-gray-500 opacity-50 aria-selected:bg-gray-500 aria-selected:text-gray-900 aria-selected:bg-opacity-10",
                                day_disabled: "text-gray-500 opacity-50",
                                day_hidden: "invisible",
                            }}
                            components={{
                                IconLeft: ({ ...props }) => (
                                    <ChevronLeftIcon {...props} className="h-4 w-4 stroke-2" />
                                ),
                                IconRight: ({ ...props }) => (
                                    <ChevronRightIcon {...props} className="h-4 w-4 stroke-2" />
                                ),
                            }}
                        />
                    </PopoverContent>
                </Popover>
            </div>
            <div className="grid grid-cols-1 mx-auto gap-4 md:grid-cols-3">
                <CardDefault />
                <CardDefault />
                <CardDefault />
            </div>
            <div className="flex items-center gap-1 md:gap-4 mt-6">
                <Button
                    variant="text"
                    className="flex items-center gap-2 "
                    onClick={prev}
                    disabled={active === 1}
                >
                    <ArrowLeftIcon strokeWidth={2} className="h-4 w-4" /> Previous
                </Button>
                <div className="flex items-center gap-2">
                    <IconButton {...getItemProps(1)}>1</IconButton>
                    <IconButton {...getItemProps(2)}>2</IconButton>
                    ...
                    <IconButton {...getItemProps(5)}>5</IconButton>
                </div>
                <Button
                    variant="text"
                    className="flex items-center gap-2"
                    onClick={next}
                    disabled={active === 5}
                >
                    Next
                    <ArrowRightIcon strokeWidth={2} className="h-4 w-4" />
                </Button>
            </div>
        </div>
    );
}

export default EventsSection;