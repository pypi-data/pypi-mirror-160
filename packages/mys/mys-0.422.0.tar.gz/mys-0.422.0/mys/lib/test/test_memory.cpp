#define CATCH_CONFIG_MAIN

#include "catch.hpp"
#include "mys/memory.hpp"
#include <unordered_set>
#include <unordered_map>

namespace mys {
void abort_is_none()
{
}
void print_traceback(void)
{
}
}

using mys::shared_ptr;
using mys::weak_ptr;
using mys::make_shared;

class Foo {
public:
    int x;

    Foo() {
        x = 5;
    }

    Foo(int y) {
        x = y;
    }

    bool __eq__(const shared_ptr<Foo>& other)
    {
        if (other) {
            return x == other->x;
        } else {
            return false;
        }
    }

    ~Foo() {
    }
};

TEST_CASE("Various")
{
    shared_ptr<Foo> a = make_shared<Foo>();
    shared_ptr<Foo> b = make_shared<Foo>(2);
    shared_ptr<Foo> c;

    REQUIRE(a == a);
    REQUIRE(a);
    REQUIRE(!c);
    REQUIRE(!(a == c));
    a = nullptr;
    c = b;
    REQUIRE(b);
    b = nullptr;
    b = nullptr;
    REQUIRE(!b);
    REQUIRE(c);
    REQUIRE(c->x == 2);
    b = c;
    REQUIRE(b->x == 2);
    b = b;
    REQUIRE(b->x == 2);

    REQUIRE(a.use_count() == 0);
    REQUIRE(b.use_count() == 2);
    REQUIRE(c.use_count() == 2);
}

class Shape {
public:
    virtual ~Shape() {
    }

    virtual int area() = 0;
};

class Box : public Shape {
public:
    ~Box() {
    }

    int area() {
        return 5;
    }
};

static int area(shared_ptr<Shape> shape)
{
    return shape->area();
}

static int area_const_ref(const shared_ptr<Shape>& shape)
{
    return shape->area();
}

TEST_CASE("Inheritance")
{
    shared_ptr<Box> box = make_shared<Box>();

    REQUIRE(box.use_count() == 1);
    REQUIRE(box->area() == 5);
    REQUIRE(area(box) == 5);
    REQUIRE(area(static_cast<shared_ptr<Shape>>(box)) == 5);
    REQUIRE(area_const_ref(box) == 5);
    REQUIRE(area_const_ref(static_cast<shared_ptr<Shape>>(box)) == 5);
    REQUIRE(box.use_count() == 1);
}

class FromThis;

class FromThisFoo {
public:
    shared_ptr<FromThis> from_this;

    FromThisFoo(shared_ptr<FromThis> from_this)
        : from_this(from_this) {
    }

    ~FromThisFoo() {
    }
};

class FromThis {
public:
    int a;
    shared_ptr<FromThisFoo> foo;

    FromThis() : a(3) {
        foo = make_shared<FromThisFoo>(shared_ptr<FromThis>(this));
    }

    ~FromThis() {
    }

    shared_ptr<FromThis> get() {
        return shared_ptr<FromThis>(this);
    }
};

TEST_CASE("Shared pointer from this")
{
    shared_ptr<FromThis> from_this = make_shared<FromThis>();

    REQUIRE(from_this->a == 3);
    REQUIRE(from_this->get()->a == 3);
    REQUIRE(from_this->foo->from_this->a == 3);
    REQUIRE(from_this->foo->from_this->get()->a == 3);
    // Break the reference cycle as there are no weak pointers.
    from_this->foo = nullptr;
}

class FromThisUseCount {
public:
    FromThisUseCount() {
    }

    ~FromThisUseCount() {
    }

    shared_ptr<FromThisUseCount> get() {
        return shared_ptr<FromThisUseCount>(this);
    }
};

TEST_CASE("Shared pointer from this use count")
{
    shared_ptr<FromThisUseCount> from_this = make_shared<FromThisUseCount>();
    shared_ptr<FromThisUseCount> from_this_2;

    REQUIRE(from_this.use_count() == 1);

    from_this = from_this;
    REQUIRE(from_this.use_count() == 1);
    REQUIRE(from_this_2.use_count() == 0);

    from_this_2 = from_this;
    REQUIRE(from_this.use_count() == 2);
    REQUIRE(from_this_2.use_count() == 2);

    from_this_2 = nullptr;
    REQUIRE(from_this.use_count() == 1);
    REQUIRE(from_this_2.use_count() == 0);

    from_this = from_this->get();
    REQUIRE(from_this.use_count() == 1);
    REQUIRE(from_this_2.use_count() == 0);
}

class NullPtr {
public:
    int a;

    NullPtr() : a(3) {
    }

    ~NullPtr() {
    }
};

static bool is_null(shared_ptr<NullPtr> null)
{
    if (null) {
        return false;
    } else {
        return true;
    }
}

TEST_CASE("Null pointer")
{
    REQUIRE(is_null(nullptr));
    REQUIRE(!is_null(make_shared<NullPtr>()));
}

static int weak_destroy_count = 0;

class WeakPtr {
public:
    weak_ptr<WeakPtr> m_parent;

    WeakPtr(const shared_ptr<WeakPtr> &parent) : m_parent(parent) {
    }

    ~WeakPtr() {
        weak_destroy_count++;
    }
};

static int shared_destroy_count = 0;

class SharedPtr {
public:
    shared_ptr<SharedPtr> m_parent;

    SharedPtr(const shared_ptr<SharedPtr> &parent) : m_parent(parent) {
    }

    ~SharedPtr() {
        shared_destroy_count++;
    }
};

static void weak()
{
    auto foo = make_shared<WeakPtr>(nullptr);
    REQUIRE(foo.count() == 1);
    REQUIRE(foo.object_count() == 1);
    REQUIRE(weak_destroy_count == 0);
    foo->m_parent = foo;
    REQUIRE(foo.count() == 2);
    REQUIRE(foo.object_count() == 1);
    REQUIRE(weak_destroy_count == 0);
}

static void shared()
{
    auto foo = make_shared<SharedPtr>(nullptr);
    REQUIRE(foo.count() == 1);
    REQUIRE(foo.object_count() == 1);
    REQUIRE(shared_destroy_count == 0);
    foo->m_parent = foo;
    REQUIRE(foo.count() == 2);
    REQUIRE(foo.object_count() == 2);
    REQUIRE(shared_destroy_count == 0);
}

TEST_CASE("Weak pointer")
{
    REQUIRE(weak_destroy_count == 0);
    weak();
    REQUIRE(weak_destroy_count == 1);

    REQUIRE(shared_destroy_count == 0);
    shared();
    REQUIRE(shared_destroy_count == 0);
}

TEST_CASE("Weak null pointer")
{
    auto foo = make_shared<NullPtr>();
    auto weak = weak_ptr(foo);
    REQUIRE(foo.count() == 2);
    REQUIRE(foo.object_count() == 1);

    weak = nullptr;
    REQUIRE(foo.count() == 1);
    REQUIRE(foo.object_count() == 1);
}

static mys::shared_ptr<int> X = mys::make_shared<int>(10);

class A {
public:
    mys::shared_ptr<int> x;

    A() {
        x = X;

        throw std::bad_alloc();
    }
};

TEST_CASE("Throw in constructor")
{
    REQUIRE(X.use_count() == 1);

    try {
        A();
    } catch (const std::bad_alloc& e) {
    }

    REQUIRE(X.use_count() == 1);

    try {
        mys::make_shared<A>();
    } catch (const std::bad_alloc& e) {
    }

    REQUIRE(X.use_count() == 1);
}

static long long begin_number_of_allocated_objects;
static long long begin_number_of_object_decrements;
static long long begin_number_of_object_frees;

static void reset_statistics()
{
    begin_number_of_allocated_objects = mys::number_of_allocated_objects;
    begin_number_of_object_decrements = mys::number_of_object_decrements;
    begin_number_of_object_frees = mys::number_of_object_frees;
}

static long long number_of_allocated_objects()
{
    return mys::number_of_allocated_objects - begin_number_of_allocated_objects;
}

static long long number_of_object_decrements()
{
    return mys::number_of_object_decrements - begin_number_of_object_decrements;
}

static long long number_of_object_frees()
{
    return mys::number_of_object_frees - begin_number_of_object_frees;
}

static void stats(shared_ptr<int> v)
{
}

static void stats_const_ref(const shared_ptr<int>& v)
{
}

TEST_CASE("Statistics 1")
{
    reset_statistics();

    {
        auto v = make_shared<int>();
        REQUIRE(number_of_allocated_objects() == 1);
        REQUIRE(number_of_object_decrements() == 0);
        REQUIRE(number_of_object_frees() == 0);

        stats(v);
        REQUIRE(number_of_allocated_objects() == 1);
        REQUIRE(number_of_object_decrements() == 1);
        REQUIRE(number_of_object_frees() == 0);

        stats_const_ref(v);
        REQUIRE(number_of_allocated_objects() == 1);
        REQUIRE(number_of_object_decrements() == 1);
        REQUIRE(number_of_object_frees() == 0);
    }

    REQUIRE(number_of_allocated_objects() == 0);
    REQUIRE(number_of_object_decrements() == 2);
    REQUIRE(number_of_object_frees() == 1);
}

TEST_CASE("Statistics 2")
{
    reset_statistics();

    auto v = make_shared<int>();
    v = nullptr;

    REQUIRE(number_of_allocated_objects() == 0);
    REQUIRE(number_of_object_decrements() == 1);
    REQUIRE(number_of_object_frees() == 1);
}

TEST_CASE("Statistics 3")
{
    reset_statistics();

    auto a = make_shared<int>();
    auto b = make_shared<int>();

    REQUIRE(number_of_allocated_objects() == 2);
    REQUIRE(number_of_object_decrements() == 0);
    REQUIRE(number_of_object_frees() == 0);

    a = b;
    REQUIRE(number_of_allocated_objects() == 1);
    REQUIRE(number_of_object_decrements() == 1);
    REQUIRE(number_of_object_frees() == 1);

    a = nullptr;
    REQUIRE(number_of_allocated_objects() == 1);
    REQUIRE(number_of_object_decrements() == 2);
    REQUIRE(number_of_object_frees() == 1);

    b = nullptr;
    REQUIRE(number_of_allocated_objects() == 0);
    REQUIRE(number_of_object_decrements() == 3);
    REQUIRE(number_of_object_frees() == 2);
}

class Item {
public:
    int m_x;

    Item(int x) : m_x(x)
    {
    }

    int __hash__(void)
    {
        return m_x;
    }

    bool __eq__(const mys::shared_ptr<Item>& other)
    {
        if (other) {
            return m_x == other->m_x;
        } else {
            return false;
        }
    }
};

TEST_CASE("Set")
{
    auto v = std::unordered_set<shared_ptr<Item>>();
    REQUIRE(v.size() == 0);
    auto a = make_shared<Item>(1);
    v.insert(a);
    v.insert(make_shared<Item>(2));
    v.insert(make_shared<Item>(3));
    v.insert(make_shared<Item>(4));
    REQUIRE(v.size() == 4);
    REQUIRE(v.find(a) != v.end());
    REQUIRE(v.find(make_shared<Item>(1)) != v.end());
}
