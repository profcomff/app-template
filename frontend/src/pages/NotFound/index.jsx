import { Button } from "@material-tailwind/react";
import { Link } from "react-router-dom";

const NotFound = () => {
    return (
        <>
            <h1 className="p-6 text-xl text-center">Nothing found :(</h1>
            <div className="flex items-center justify-center">
                <Link to='/'>
                    <Button>Go to home page</Button>
                </Link>
            </div>
        </>
    );
}

export default NotFound;